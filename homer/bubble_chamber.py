import random
import statistics
from typing import List, Union

from .errors import MissingStructureError
from .id import ID
from .logger import Logger
from .problem import Problem
from .structure_collection import StructureCollection
from .structures import Chunk, Space
from .structures.chunks import View, Word
from .structures.links import Correspondence, Label, Relation
from .structures.spaces import ConceptualSpace, WorkingSpace


class BubbleChamber:
    def __init__(
        self,
        conceptual_spaces: StructureCollection,
        working_spaces: StructureCollection,
        chunks: StructureCollection,
        concepts: StructureCollection,
        correspondences: StructureCollection,
        labels: StructureCollection,
        relations: StructureCollection,
        views: StructureCollection,
        words: StructureCollection,
        concept_links: StructureCollection,
        slots: StructureCollection,
        logger: Logger,
    ):
        self.conceptual_spaces = conceptual_spaces
        self.working_spaces = working_spaces
        self.chunks = chunks
        self.concepts = concepts
        self.correspondences = correspondences
        self.labels = labels
        self.relations = relations
        self.views = views
        self.words = words
        self.concept_links = concept_links
        self.slots = slots
        self.logger = logger
        self.result = None

    @property
    def spaces(self):
        return StructureCollection.union(self.conceptual_spaces, self.working_spaces)

    @property
    def structures(self):
        return StructureCollection.union(
            self.conceptual_spaces,
            self.working_spaces,
            self.chunks,
            self.concepts,
            self.correspondences,
            self.labels,
            self.relations,
            self.views,
            self.words,
            self.concept_links,
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
            self.logger.log(structure)

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

    def common_parent_space(self, space_one: Space, space_two: Space):
        try:
            parent_space = StructureCollection.intersection(
                space_one.parent_spaces, space_two.parent_spaces
            ).get_random()
        except MissingStructureError:
            parent_space = WorkingSpace(
                ID.new(WorkingSpace),
                "",
                space_one.name + " x " + space_two.name,
                StructureCollection(),
                0,
                None,
                child_spaces=StructureCollection({space_one, space_two}),
            )
            self.working_spaces.add(parent_space)
            space_one.parent_spaces.add(parent_space)
            space_two.parent_spaces.add(parent_space)
        return parent_space
