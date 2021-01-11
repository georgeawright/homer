import random
import statistics
from typing import List, Union

from .errors import MissingStructureError
from .id import ID
from .location import Location
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
        frames: StructureCollection,
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
        self.frames = frames
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
        return StructureCollection.union(
            self.conceptual_spaces, self.working_spaces, self.frames
        )

    @property
    def structures(self):
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

    def get_super_space(self, space_one: Space, space_two: Space) -> WorkingSpace:
        for space in self.working_spaces:
            try:
                if (
                    space.dimensions == space_one.dimensions + space_two.dimensions
                    or space.dimensions == space_two.dimensions + space_one.dimensions
                ):
                    print("found super space")
                    print(space.name)
                    print(space.dimensions)
                    print(f"{space_one.dimensions} + {space_two.dimensions}")
                    return space
            except Exception:
                print("not found super space")
                pass
        super_space = WorkingSpace(
            ID.new(WorkingSpace),
            "",
            f"{space_one.name} x {space_two.name}",
            None,
            None,
            [Location([], self.spaces["top level working"])],
            StructureCollection(),
            space_one.no_of_dimensions + space_two.no_of_dimensions,
            space_one.dimensions + space_two.dimensions,
            [space_one, space_two],
            0,
        )
        space_one.super_space_to_coordinate_function_map[
            super_space.name
        ] = lambda location: location.coordinates[: space_one.no_of_dimensions]
        space_two.super_space_to_coordinate_function_map[
            super_space.name
        ] = lambda location: location.coordinates[space_one.no_of_dimensions :]
        self.working_spaces.add(super_space)
        self.logger.log(super_space)
        return super_space
