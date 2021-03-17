import operator
from typing import Any, Callable, Dict, List, Union

from homer import fuzzy
from .bubble_chamber import BubbleChamber
from .classifier import Classifier
from .coderack import Coderack
from .errors import MissingStructureError, NoMoreCodelets
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .id import ID
from .location import Location
from .logger import Logger
from .loggers import DjangoLogger
from .problem import Problem
from .structure import Structure
from .structure_collection import StructureCollection
from .structures import Space, View
from .structures.links import Correspondence, Label, Relation
from .structures.nodes import Chunk, Concept, Lexeme, Rule, Word
from .structures.spaces import ConceptualSpace, WorkingSpace
from .structures.spaces.frames import Template
from .word_form import WordForm


class Homer:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        logger: Logger,
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.logger = logger
        self.activation_update_frequency = activation_update_frequency

    @classmethod
    def setup(cls, logger: Logger):
        top_level_conceptual_space = ConceptualSpace(
            "top_level_space",
            "",
            "top level",
            None,
            [None],
            StructureCollection(),
            0,
            [],
            [],
        )
        logger.log(top_level_conceptual_space)
        top_level_working_space = top_level_conceptual_space.instance_in_space(
            None, name="top level working"
        )
        logger.log(top_level_working_space)
        bubble_chamber = BubbleChamber(
            StructureCollection({top_level_conceptual_space}),
            StructureCollection({top_level_working_space}),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            logger,
        )
        bubble_chamber.lexemes = StructureCollection()
        coderack = Coderack.setup(bubble_chamber, logger)
        return cls(bubble_chamber, coderack, logger)

    def run(self):
        while self.bubble_chamber.result is None:
            self.logger.log(self.coderack)
            if self.coderack.codelets_run % self.activation_update_frequency == 0:
                self.print_status_update()
                self.bubble_chamber.spread_activations()
                self.bubble_chamber.update_activations()
            try:
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.logger.log("no more codelets")
                self.print_results()
                break
            except Exception as e:
                raise e
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        bubble_chamber_satisfaction = self.bubble_chamber.satisfaction
        build_activation = self.bubble_chamber.concepts["build"].activation
        evaluate_activation = self.bubble_chamber.concepts["evaluate"].activation
        select_activation = self.bubble_chamber.concepts["select"].activation
        print(
            "================================================================================"
        )
        print(
            f"codelets run: {codelets_run}; "
            + f"satisfaction: {bubble_chamber_satisfaction}; "
            + f"build: {build_activation}; "
            + f"evaluate: {evaluate_activation}; "
            + f"select: {select_activation}; "
        )
        print(
            "================================================================================"
        )

    def print_results(self):
        print("results go here")

    def def_concept(
        self,
        name: str = "",
        prototype: Any = None,
        classifier: Classifier = None,
        parent_space: ConceptualSpace = None,
        relevant_value: str = "",
        instance_type: type = List[int],
        child_spaces: StructureCollection = None,
        distance_function: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        depth: int = 1,
        activation: float = 0.0,
    ) -> Concept:
        location = (
            Location(prototype, parent_space)
            if prototype is not None
            else Location([], parent_space)
        )
        concept = Concept(
            structure_id=ID.new(Concept),
            parent_id="",
            name=name,
            location=location,
            classifier=classifier,
            relevant_value=relevant_value,
            instance_type=instance_type,
            child_spaces=(
                child_spaces if child_spaces is not None else StructureCollection()
            ),
            distance_function=distance_function,
            links_in=links_in,
            links_out=links_out,
            depth=depth,
        )
        concept._activation = activation
        parent_space.add(concept)
        self.logger.log(concept)
        self.bubble_chamber.concepts.add(concept)
        return concept

    def def_conceptual_space(
        self,
        name: str = "",
        parent_concept: Concept = None,
        locations: List[Location] = None,
        contents: StructureCollection = None,
        no_of_dimensions: int = 0,
        dimensions: List[ConceptualSpace] = None,
        sub_spaces: List[ConceptualSpace] = None,
        is_basic_level: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ) -> ConceptualSpace:
        conceptual_space = ConceptualSpace(
            structure_id=ID.new(ConceptualSpace),
            parent_id="",
            name=name,
            parent_concept=parent_concept,
            locations=(locations if locations is not None else []),
            contents=(contents if contents is not None else StructureCollection()),
            no_of_dimensions=no_of_dimensions,
            dimensions=(dimensions if dimensions is not None else []),
            sub_spaces=(sub_spaces if sub_spaces is not None else []),
            is_basic_level=is_basic_level,
            super_space_to_coordinate_function_map=super_space_to_coordinate_function_map,
            links_in=links_in,
            links_out=links_out,
        )
        self.logger.log(conceptual_space)
        if parent_concept is not None:
            parent_concept.child_spaces.add(conceptual_space)
        for location in locations:
            if location is None:
                continue
            location.space.add(conceptual_space)
        self.bubble_chamber.conceptual_spaces.add(conceptual_space)
        return conceptual_space

    def def_concept_link(
        self,
        start: Concept,
        end: Concept,
        activation: FloatBetweenOneAndZero = 0.0,
        stable: bool = False,
    ) -> Relation:
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id="",
            start=start,
            end=end,
            parent_concept=None,
            parent_space=None,
            quality=1.0,
        )
        relation._activation = activation
        relation.stable = stable
        start.links_out.add(relation)
        end.links_in.add(relation)
        self.logger.log(relation)
        self.bubble_chamber.concept_links.add(relation)
        return relation

    def def_lexeme(
        self,
        headword: str = "",
        forms: Dict[str, str] = None,
        parts_of_speech: Dict[WordForm, List[Concept]] = None,
        parent_concept: Concept = None,
    ) -> Lexeme:
        if operator.xor(forms is None, parts_of_speech is None) or (
            forms.keys() != parts_of_speech.keys()
        ):
            raise Exception("lexeme forms and parts of speech do not match")
        lexeme = Lexeme(
            structure_id=ID.new(Lexeme),
            parent_id="",
            headword=headword,
            forms=forms,
            parts_of_speech=parts_of_speech,
        )
        self.logger.log(lexeme)
        self.bubble_chamber.lexemes.add(lexeme)
        if parent_concept is not None:
            link_to_concept = self.def_concept_link(
                parent_concept, lexeme, activation=1.0
            )
            parent_concept.links_out.add(link_to_concept)
            lexeme.links_in.add(link_to_concept)
        return lexeme

    def def_template(
        self,
        name: str = "",
        parent_concept: Concept = None,
        conceptual_space: ConceptualSpace = None,
        contents: List[Word] = None,
    ) -> Template:
        template = Template(
            structure_id=ID.new(Template),
            parent_id="",
            name=name,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            locations=[Location([], self.bubble_chamber.spaces["templates"])],
            contents=StructureCollection(),
        )
        self.logger.log(template)
        for i, item in enumerate(contents):
            item.parent_space = template
            item.locations = [Location([i], template)]
            template.contents.add(item)
            self.logger.log(item)
        self.bubble_chamber.conceptual_spaces.add(template)
        self.bubble_chamber.frames.add(template)
        return template

    def def_word(
        self,
        lexeme: Lexeme = None,
        word_form: WordForm = WordForm.HEADWORD,
        quality: FloatBetweenOneAndZero = 1.0,
    ):
        word = Word(
            structure_id=ID.new(Word),
            parent_id="",
            lexeme=lexeme,
            word_form=word_form,
            location=None,
            parent_space=None,
            quality=quality,
        )
        return word

    def def_working_space(
        self,
        name: str = "",
        parent_concept: Concept = None,
        conceptual_space: ConceptualSpace = None,
        locations: List[Location] = None,
        contents: StructureCollection = None,
        no_of_dimensions: int = 0,
        dimensions: List[WorkingSpace] = None,
        sub_spaces: List[WorkingSpace] = None,
        is_basic_level: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ) -> WorkingSpace:
        working_space = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id="",
            name=name,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            locations=(locations if locations is not None else []),
            contents=(contents if contents is not None else StructureCollection()),
            no_of_dimensions=no_of_dimensions,
            dimensions=(dimensions if dimensions is not None else []),
            sub_spaces=(sub_spaces if sub_spaces is not None else []),
            is_basic_level=is_basic_level,
            super_space_to_coordinate_function_map=super_space_to_coordinate_function_map,
            links_in=links_in,
            links_out=links_out,
        )
        self.logger.log(working_space)
        for location in locations:
            if location is None:
                continue
            location.space.add(working_space)
        self.bubble_chamber.working_spaces.add(working_space)
        return working_space

    def def_correspondence(
        self,
        start: Structure,
        end: Structure,
        start_space: Space = None,
        end_space: Space = None,
        locations: List[Location] = None,
        parent_concept: Concept = None,
        conceptual_space: ConceptualSpace = None,
        parent_view: View = None,
        is_privileged: bool = True,
        stable: bool = True,
    ) -> Correspondence:
        start_space = start.location.space if start_space is None else start_space
        end_space = end.location.space if end_space is None else end_space
        locations = (
            [start.location_in_space(start_space), end.location_in_space(end_space)]
            if locations is None
            else locations
        )
        parent_concept = (
            self.bubble_chamber.concepts["same"]
            if parent_concept is None
            else parent_concept
        )
        conceptual_space = (
            self.bubble_chamber.conceptual_spaces["text"]
            if conceptual_space is None
            else conceptual_space
        )
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id="",
            start=start,
            end=end,
            start_space=start_space,
            end_space=end_space,
            locations=locations,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            parent_view=parent_view,
            quality=1,
            is_privileged=is_privileged,
        )
        correspondence._activation = 1
        correspondence.stable = stable
        start.links_out.add(correspondence)
        start.links_in.add(correspondence)
        end.links_out.add(correspondence)
        end.links_in.add(correspondence)
        self.logger.log(correspondence)
        for location in locations:
            location.space.add(correspondence)
        return correspondence

    def def_chunk(
        self,
        value: Any = None,
        locations: List[Location] = None,
        members: StructureCollection = None,
        parent_space: WorkingSpace = None,
        quality: FloatBetweenOneAndZero = 1,
    ):
        locations = locations if locations is not None else []
        members = members if members is not None else StructureCollection()
        chunk = Chunk(
            ID.new(Chunk),
            "",
            value=value,
            locations=locations,
            members=members,
            parent_space=parent_space,
            quality=quality,
        )
        for location in locations:
            location.space.add(chunk)
        if not chunk.is_slot:
            self.bubble_chamber.chunks.add(chunk)
        self.logger.log(chunk)
        return chunk

    def def_label(
        self,
        start: Structure = None,
        parent_concept: Concept = None,
        parent_space: WorkingSpace = None,
        quality: FloatBetweenOneAndZero = 1,
    ):
        label = Label(
            ID.new(Label),
            "",
            start=start,
            parent_concept=parent_concept,
            parent_space=parent_space,
            quality=quality,
        )
        start.links_out.add(label)
        if not label.is_slot:
            self.bubble_chamber.labels.add(label)
        self.logger.log(label)
        return label

    def def_relation(
        self,
        start: Structure = None,
        end: Structure = None,
        parent_concept: Concept = None,
        parent_space: Space = None,
        quality: FloatBetweenOneAndZero = 1,
    ):
        relation = Relation(
            ID.new(Relation),
            "",
            start=start,
            end=end,
            parent_concept=parent_concept,
            parent_space=parent_space,
            quality=quality,
        )
        start.links_out.add(relation)
        start.links_in.add(relation)
        if not relation.is_slot:
            self.bubble_chamber.relations.add(relation)
        self.logger.log(relation)
        return relation

    def def_rule(
        self,
        name: str,
        location: Location,
        root: Concept,
        left_branch: Concept,
        right_branch: Concept,
        stable_activation: FloatBetweenOneAndZero = None,
    ):
        rule = Rule(
            ID.new(Rule),
            "",
            name,
            location,
            root,
            left_branch,
            right_branch,
            stable_activation=stable_activation,
        )
        self.logger.log(rule)
        root_link = self.def_concept_link(root, rule, stable_activation, True)
        left_link = self.def_concept_link(rule, left_branch, stable_activation, True)
        right_link = self.def_concept_link(rule, right_branch, stable_activation, True)
        self.logger.log(rule)
