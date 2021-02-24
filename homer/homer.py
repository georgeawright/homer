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
from .structures import Space
from .structures.links import Correspondence, Relation
from .structures.nodes import Concept, Lexeme, Word
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
        parent_concept: Concept = None,
    ) -> Lexeme:
        lexeme = Lexeme(
            structure_id=ID.new(Lexeme),
            parent_id="",
            headword=headword,
            forms=forms,
        )
        self.logger.log(lexeme)
        self.bubble_chamber.lexemes.add(lexeme)
        link_to_concept = self.def_concept_link(parent_concept, lexeme, activation=1.0)
        parent_concept.links_out.add(link_to_concept)
        lexeme.links_in.add(link_to_concept)
        return lexeme

    def def_template(
        self,
        name: str = "",
        parent_concept: Concept = None,
        contents: List[Word] = None,
    ) -> Template:
        template = Template(
            structure_id=ID.new(Template),
            parent_id="",
            name=name,
            parent_concept=parent_concept,
            locations=[Location([], self.bubble_chamber.spaces["templates"])],
            contents=StructureCollection(),
        )
        self.logger.log(template)
        for i, item in enumerate(contents):
            item.parent_space = template
            item.locations = [Location([i], template)]
            template.contents.add(item)
            self.logger.log(item)
            if item.is_slot:
                try:
                    working_space = (
                        template.contents.of_type(WorkingSpace)
                        .where(parent_concept=item.value)
                        .get_random()
                    )
                except MissingStructureError:
                    conceptual_space = self.bubble_chamber.conceptual_spaces[
                        item.value.name
                    ]
                    working_space = conceptual_space.instance_in_space(template)
                    self.logger.log(working_space)
                    template.add(working_space)
                filler_coordinates = [0 for _ in conceptual_space.dimensions]
                item.locations.append(Location(filler_coordinates, working_space))
                working_space.add(item)
                self.logger.log(item)
                self.def_concept_link(item.value, item, activation=1.0, stable=True)
        self.bubble_chamber.conceptual_spaces.add(template)
        self.bubble_chamber.frames.add(template)
        return template

    def def_template_slot(self, concept: Concept = None, form: WordForm = None):
        slot = None  # TODO
        self.bubble_chamber.slots.add(slot)
        return slot

    def def_word(
        self,
        value: str = "",
        lexeme: Lexeme = None,
        quality: FloatBetweenOneAndZero = 1.0,
    ):
        word = Word(
            structure_id=ID.new(Word),
            parent_id="",
            parent_space=None,
            value=value,
            lexeme=lexeme,
            location=None,
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
        location: Location = None,
        start_space: Space = None,
        end_space: Space = None,
        parent_concept: Concept = None,
        conceptual_space: ConceptualSpace = None,
        is_privileged: bool = True,
        stable: bool = True,
    ) -> Correspondence:
        start_space = start.location.space if start_space is None else start_space
        end_space = end.location.space if end_space is None else end_space
        location = start.location if location is None else location
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
            location=location,
            start_space=start_space,
            end_space=end_space,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
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
        location.space.add(correspondence)
        return correspondence
