import random
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
        working_spaces: StructureCollection,
        frames: StructureCollection,
        chunks: StructureCollection,
        concepts: StructureCollection,
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
        self.working_spaces = working_spaces
        self.frames = frames
        self.chunks = chunks
        self.concepts = concepts
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
        return self.words

    @property
    def structures(self) -> StructureCollection:
        return StructureCollection.union(
            self.conceptual_spaces,
            self.working_spaces,
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
        return self.working_spaces["top level working"].quality

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
            if self.log_count % 25 == 0:
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
