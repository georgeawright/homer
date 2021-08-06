from itertools import chain
import statistics
from typing import List, Union

from .errors import MissingStructureError
from .id import ID
from .location import Location
from .logger import Logger
from .problem import Problem
from .structure_collection import StructureCollection
from .structures import Space, View
from .structures.links import Correspondence, Label, Relation
from .structures.nodes import Chunk, Word
from .structures.spaces import ConceptualSpace, WorkingSpace


class BubbleChamber:
    def __init__(
        self,
        conceptual_spaces: StructureCollection,
        contextual_spaces: StructureCollection,
        frames: StructureCollection,
        frame_instances: StructureCollection,
        chunks: StructureCollection,
        concepts: StructureCollection,
        lexemes: StructureCollection,
        correspondences: StructureCollection,
        labels: StructureCollection,
        relations: StructureCollection,
        views: StructureCollection,
        words: StructureCollection,
        concept_links: StructureCollection,
        phrases: StructureCollection,
        rules: StructureCollection,
        slots: StructureCollection,
        logger: Logger,
    ):
        self.conceptual_spaces = conceptual_spaces
        self.contextual_spaces = contextual_spaces
        self.frames = frames
        self.frame_instances = frame_instances
        self.chunks = chunks
        self.concepts = concepts
        self.lexemes = lexemes
        self.correspondences = correspondences
        self.labels = labels
        self.relations = relations
        self.views = views
        self.words = words
        self.concept_links = concept_links
        self.phrases = phrases
        self.rules = rules
        self.slots = slots
        self.logger = logger
        self.log_count = 0
        self.result = None

    @classmethod
    def setup(cls, logger: Logger):
        return cls(
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
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            logger,
        )

    @property
    def spaces(self) -> StructureCollection:
        return StructureCollection.union(
            self.conceptual_spaces, self.working_spaces, self.frames
        )

    @property
    def text_fragments(self) -> StructureCollection:
        return StructureCollection.union(self.phrases, self.words)

    @property
    def input_nodes(self) -> StructureCollection:
        return StructureCollection(
            {
                node
                for node in chain(self.chunks, self.words)
                if node.parent_space.parent_concept
                in (self.concepts["input"], self.concepts["text"])
                and not node.parent_space.is_frame
            }
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
            self.phrases,
            self.rules,
            self.slots,
        )

    @property
    def satisfaction(self):
        return statistics.fmean([space.quality for space in self.contextual_spaces])

    def add_to_collections(self, item):
        collections = {
            Chunk: self.chunks,
            Correspondence: self.correspondences,
            Label: self.labels,
            Relation: self.relations,
            View: self.views,
            Word: self.words,
        }
        collections[type(item)].add(item)

    def spread_activations(self):
        for structure in self.structures:
            structure.spread_activation()

    def update_activations(self) -> None:
        for structure in self.structures:
            structure.update_activation()
            if self.log_count % 500 == 0:
                self.logger.log(structure)
        self.log_count += 1

    def has_chunk(self, members: StructureCollection) -> bool:
        for chunk in self.chunks:
            if chunk.members == members:
                return True
        return False

    def has_view(self, members: StructureCollection) -> bool:
        for view in self.views:
            if view.members == members:
                return True
        return False
