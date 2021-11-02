from itertools import chain
import statistics
from typing import Callable, Dict, List, Union

from .classifier import Classifier
from .errors import MissingStructureError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .id import ID
from .location import Location
from .logger import Logger
from .problem import Problem
from .random_machine import RandomMachine
from .structure import Structure
from .structure_collection import StructureCollection
from .structures import Space, View
from .structures.links import Correspondence, Label, Relation
from .structures.nodes import Chunk, Concept, Lexeme, Rule, Word
from .structures.spaces import ConceptualSpace, ContextualSpace, Frame
from .structures.views import SimplexView, MonitoringView
from .word_form import WordForm


class BubbleChamber:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.random_machine = None

        self.conceptual_spaces = None
        self.contextual_spaces = None
        self.frames = None
        self.frame_instances = None

        self.concepts = None
        self.lexemes = None
        self.chunks = None
        self.words = None
        self.rules = None

        self.concept_links = None
        self.correspondences = None
        self.labels = None
        self.relations = None

        self.views = None

        self.result = None
        self.log_count = 0

    @classmethod
    def setup(cls, logger: Logger, random_seed: int = None):
        bubble_chamber = cls(logger)
        bubble_chamber.random_machine = RandomMachine(bubble_chamber, random_seed)
        bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection()
        bubble_chamber.contextual_spaces = bubble_chamber.new_structure_collection()
        bubble_chamber.frames = bubble_chamber.new_structure_collection()
        bubble_chamber.frame_instances = bubble_chamber.new_structure_collection()
        bubble_chamber.concepts = bubble_chamber.new_structure_collection()
        bubble_chamber.lexemes = bubble_chamber.new_structure_collection()
        bubble_chamber.chunks = bubble_chamber.new_structure_collection()
        bubble_chamber.words = bubble_chamber.new_structure_collection()
        bubble_chamber.rules = bubble_chamber.new_structure_collection()
        bubble_chamber.concept_links = bubble_chamber.new_structure_collection()
        bubble_chamber.correspondences = bubble_chamber.new_structure_collection()
        bubble_chamber.labels = bubble_chamber.new_structure_collection()
        bubble_chamber.relations = bubble_chamber.new_structure_collection()
        bubble_chamber.views = bubble_chamber.new_structure_collection()
        return bubble_chamber

    @property
    def spaces(self) -> StructureCollection:
        return StructureCollection.union(
            self.conceptual_spaces, self.contextual_spaces, self.frames
        )

    @property
    def input_nodes(self) -> StructureCollection:
        return self.new_structure_collection(
            *[
                node
                for node in chain(self.chunks, self.words)
                if node.parent_space.parent_concept
                in (self.concepts["input"], self.concepts["text"])
                and not node.parent_space.is_frame
            ]
        )

    @property
    def comprehension_views(self) -> StructureCollection:
        return self.monitoring_views

    @property
    def production_views(self) -> StructureCollection:
        return StructureCollection.union(self.discourse_views, self.simplex_views)

    @property
    def monitoring_views(self) -> StructureCollection:
        return self.views.where(is_monitoring_view=True)

    @property
    def discourse_views(self) -> StructureCollection:
        return self.views.where(is_discourse_view=True)

    @property
    def simplex_views(self) -> StructureCollection:
        return self.views.where(is_simplex_view=True)

    @property
    def structures(self) -> StructureCollection:
        return StructureCollection.union(
            self.conceptual_spaces,
            self.contextual_spaces,
            self.frames,
            self.chunks,
            self.concepts,
            self.correspondences,
            self.labels,
            self.relations,
            self.views,
            self.words,
            self.concept_links,
            self.rules,
        )

    @property
    def satisfaction(self):
        return statistics.fmean([space.quality for space in self.contextual_spaces])

    def spread_activations(self):
        for structure in self.structures:
            structure.spread_activation()

    def update_activations(self) -> None:
        for structure in self.structures:
            structure.update_activation()
            if self.log_count % 500 == 0:
                self.logger.log(structure)
        self.log_count += 1

    def new_structure_collection(
        self, *structures: List[Structure]
    ) -> StructureCollection:
        return StructureCollection(self, structures)

    def add(self, item):
        self.logger.log(item)
        for space in item.parent_spaces:
            space.add(item)
            self.logger.log(space)
        collections = {
            # views
            MonitoringView: self.monitoring_views,
            SimplexView: self.simplex_views,
            # spaces
            ConceptualSpace: self.conceptual_spaces,
            ContextualSpace: self.contextual_spaces,
            Frame: self.frames,
            # nodes
            Chunk: self.chunks,
            Concept: self.concepts,
            Lexeme: self.lexemes,
            Rule: self.rules,
            Word: self.words,
            # links
            Correspondence: self.correspondences,
            Label: self.labels,
            Relation: self.relations,
        }
        collections[type(item)].add(item)

    def new_conceptual_space(
        self,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        no_of_dimensions: int,
        dimensions: List[ConceptualSpace],
        sub_spaces: List[ConceptualSpace],
        is_basic_level: bool = False,
        is_symbolic: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
    ) -> ConceptualSpace:
        space = ConceptualSpace(
            structure_id=ID.new(ConceptualSpace),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=self.new_structure_collection(),
            no_of_dimensions=no_of_dimensions,
            dimensions=dimensions,
            sub_spaces=sub_spaces,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
            is_basic_level=is_basic_level,
            is_symbolic=is_symbolic,
            super_space_to_coordinate_function_map=super_space_to_coordinate_function_map,
        )
        self.add(space)
        return space

    def new_contextual_space(
        self,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        conceptual_spaces: StructureCollection,
    ) -> ContextualSpace:
        space = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=self.new_structure_collection(),
            conceptual_spaces=conceptual_spaces,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
        )
        self.add(space)
        return space

    def new_frame(
        self,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureCollection,
        input_space: ContextualSpace,
        output_space: ContextualSpace,
    ) -> Frame:
        frame = Frame(
            structure_id=ID.new(Frame),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=contents,
            input_space=input_space,
            output_space=output_space,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
        )
        self.add(frame)
        return frame

    def new_chunk(
        self,
        parent_id: str,
        locations: List[Location],
        members: StructureCollection,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        left_branch: StructureCollection,
        right_branch: StructureCollection,
        rule: Rule,
        is_raw: bool = False,
    ) -> Chunk:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        chunk = Chunk(
            structure_id=ID.new(Chunk),
            parent_id=parent_id,
            locations=locations,
            members=members,
            parent_space=parent_space,
            quality=quality,
            left_branch=left_branch,
            right_branch=right_branch,
            rule=rule,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            super_chunks=self.new_structure_collection(),
            is_raw=is_raw,
        )
        for member in members:
            member.super_chunks.add(chunk)
        self.add(chunk)
        return chunk

    def new_concept(
        self,
        parent_id: str,
        name: str,
        locations: List[Location],
        classifier: Classifier,
        instance_type: type,
        structure_type: type,
        parent_space: Space,
        distance_function: Callable,
        depth: int = 1,
        distance_to_proximity_weight: float = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT,
    ) -> Concept:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        concept = Concept(
            structure_id=ID.new(Concept),
            parent_id=parent_id,
            name=name,
            locations=locations,
            classifier=classifier,
            instance_type=instance_type,
            structure_type=structure_type,
            parent_space=parent_space,
            child_spaces=self.new_structure_collection(),
            distance_function=distance_function,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            depth=depth,
            distance_to_proximity_weight=distance_to_proximity_weight,
        )
        self.add(concept)
        return concept

    def new_lexeme(
        self,
        parent_id: str,
        headword: str,
        word_forms: dict,
        concepts: List[Concept] = None,
    ) -> Lexeme:
        concepts = [] if concepts is None else concepts
        lexeme = Lexeme(
            structure_id=ID.new(Lexeme),
            parent_id=parent_id,
            headword=headword,
            word_forms=word_forms,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
        )
        self.add(lexeme)
        for concept in concepts:
            self.new_relation(
                parent_id=parent_id,
                start=concept,
                end=lexeme,
                parent_concept=None,
                locations=[],
                quality=1.0,
            )
        return lexeme

    def new_rule(
        self,
        parent_id: str,
        name: str,
        location: Location,
        root_concept: Concept,
        left_concept: Concept,
        right_concept: Concept,
        stable_activation: FloatBetweenOneAndZero = None,
    ) -> Rule:
        rule = Rule(
            structure_id=ID.new(Rule),
            parent_id=parent_id,
            name=name,
            location=location,
            root_concept=root_concept,
            left_concept=left_concept,
            right_concept=right_concept,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(location.space),
            stable_activation=stable_activation,
        )
        self.new_relation(
            parent_id=parent_id,
            start=root_concept,
            end=rule,
            parent_concept=None,
            locations=[],
            quality=1.0,
        )
        self.new_relation(
            parent_id=parent_id,
            start=rule,
            end=left_concept,
            parent_concept=None,
            locations=[],
            quality=1.0,
        )
        if right_concept is not None:
            self.new_relation(
                parent_id=parent_id,
                start=rule,
                end=right_concept,
                parent_concept=None,
                locations=[],
                quality=1.0,
            )
        self.add(rule)
        return rule

    def new_word(
        self,
        parent_id: str,
        name: str,
        lexeme: Union[Lexeme, None],
        word_form: WordForm,
        locations: List[Location],
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
    ) -> Word:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        word = Word(
            structure_id=ID.new(Word),
            parent_id=parent_id,
            name=name,
            lexeme=lexeme,
            word_form=word_form,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            super_chunks=self.new_structure_collection(),
        )
        self.add(word)
        return word

    def new_correspondence(
        self,
        parent_id: str,
        start: Structure,
        end: Structure,
        locations: List[Location],
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        parent_view: View,
        quality: FloatBetweenOneAndZero,
        is_privileged: bool = False,
    ) -> Correspondence:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=parent_id,
            start=start,
            arguments=self.new_structure_collection(start, end),
            locations=locations,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            parent_view=parent_view,
            quality=quality,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            is_privileged=is_privileged,
        )
        if parent_view is not None:
            parent_view.members.add(correspondence)
        start.links_out.add(correspondence)
        start.links_in.add(correspondence)
        end.links_out.add(correspondence)
        end.links_in.add(correspondence)
        self.add(correspondence)
        self.logger.log(start)
        self.logger.log(end)
        return correspondence

    def new_label(
        self,
        parent_id: str,
        start: Structure,
        parent_concept: Concept,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
    ) -> Label:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        label = Label(
            structure_id=ID.new(Label),
            parent_id=parent_id,
            start=start,
            arguments=self.new_structure_collection(start),
            parent_concept=parent_concept,
            locations=locations,
            quality=quality,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
        )
        start.links_out.add(label)
        self.add(label)
        self.logger.log(start)
        return label

    def new_relation(
        self,
        parent_id: str,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        is_bidirectional: bool = True,
    ) -> Relation:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=parent_id,
            start=start,
            arguments=self.new_structure_collection(start, end),
            parent_concept=parent_concept,
            locations=locations,
            quality=quality,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            is_bidirectional=is_bidirectional,
        )
        start.links_out.add(relation)
        end.links_in.add(relation)
        self.add(relation)
        self.logger.log(start)
        self.logger.log(end)
        return relation

    def new_simplex_view(self) -> SimplexView:
        raise NotImplementedError

    def new_monitoring_view(self) -> MonitoringView:
        raise NotImplementedError
