import random
import statistics
from typing import List, Union

from .errors import MissingStructureError
from .logger import Logger
from .problem import Problem
from .structure_collection import StructureCollection
from .structures import Space
from .structures.spaces import ConceptualSpace, WorkingSpace


class BubbleChamber:
    def __init__(
        self,
        top_level_working_space: Space,
        top_level_conceptual_space: Space,
        chunks: StructureCollection,
        concepts: StructureCollection,
        correspondences: StructureCollection,
        labels: StructureCollection,
        relations: StructureCollection,
        spaces: StructureCollection,
        views: StructureCollection,
        words: StructureCollection,
        logger: Logger,
    ):
        self.top_level_working_space = top_level_working_space
        self.top_level_conceptual_space = top_level_conceptual_space
        self.chunks = chunks
        self.concepts = concepts
        self.correspondences = correspondences
        self.labels = labels
        self.relations = relations
        self.spaces = spaces
        self.views = views
        self.words = words
        self.logger = logger
        self.result = None

    @property
    def structures(self):
        return StructureCollection.union(
            self.chunks,
            self.concepts,
            self.correspondences,
            self.labels,
            self.relations,
            self.spaces,
            self.views,
            self.words,
        )

    @property
    def working_spaces(self):
        return StructureCollection(
            {space for space in self.spaces if isinstance(space, WorkingSpace)}
        )

    @property
    def satisfaction(self):
        return self.top_level_working_space.quality

    def spread_activations(self):
        for structure in self.structures:
            structure.spread_activation()

    def update_activations(self) -> None:
        for structure in self.structures:
            structure.update_activation()

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
                space_one.name + " x " + space_two.name,
                StructureCollection(),
                0,
                None,
                child_spaces=StructureCollection({space_one, space_two}),
            )
            self.spaces.add(parent_space)
            space_one.parent_spaces.add(parent_space)
            space_two.parent_spaces.add(parent_space)
        return parent_space
