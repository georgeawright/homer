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

    def new_frame(self) -> Frame:
        raise NotImplementedError

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
            link = Relation(
                "",
                "",
                concept,
                self.new_structure_collection(concept, lexeme),
                None,
                [],
                1.0,
                self.new_structure_collection(),
                self.new_structure_collection(),
                self.new_structure_collection(),
            )
            concept.links_out.add(link)
            lexeme.links_in.add(link)
            self.add(link)
        return lexeme

    def new_rule(self) -> Rule:
        raise NotImplementedError

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

    def new_correspondence(self) -> Correspondence:
        raise NotImplementedError

    def new_label(self) -> Label:
        raise NotImplementedError

    def new_relation(self) -> Relation:
        raise NotImplementedError

    def new_simplex_view(self) -> SimplexView:
        raise NotImplementedError

    def new_monitoring_view(self) -> MonitoringView:
        raise NotImplementedError
