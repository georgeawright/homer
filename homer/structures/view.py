from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept
from homer.structures.space import Space
from homer.structures.spaces import Frame, WorkingSpace


class View(Structure):
    """A collection of spaces and self-consistent correspondences between them."""

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        location: Location,
        members: StructureCollection,
        input_spaces: StructureCollection,
        output_space: WorkingSpace,
        quality: FloatBetweenOneAndZero,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations=[location],
            quality=quality,
        )
        self.value = None
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.slot_values = {}
        self.is_view = True

    @property
    def input_working_spaces(self):
        return StructureCollection(
            {space for space in self.input_spaces if not isinstance(space, Frame)}
        )

    @property
    def input_frames(self):
        return StructureCollection(
            {space for space in self.input_spaces if isinstance(space, Frame)}
        )

    @property
    def size(self):
        return len(self.members)

    @property
    def slots(self):
        # TODO: ideally there should be a recursive call to space.slots
        spaces = StructureCollection.union(
            self.input_spaces,
            StructureCollection(
                {
                    sub_space
                    for space in self.input_spaces
                    for sub_space in space.contents.where(is_space=True)
                }
            ),
        )
        return StructureCollection(
            {
                structure
                for space in spaces
                for structure in space.contents
                if structure.is_slot
            }
        )

    def copy(self, **kwargs: dict):
        raise NotImplementedError

    def has_member(
        self,
        parent_concept: Concept,
        start: Structure,
        end: Structure,
        start_space: Space,
        end_space: Space,
    ) -> bool:
        for correspondence in self.members:
            if (
                correspondence.parent_concept == parent_concept
                and correspondence.start == start
                and correspondence.end == end
                and correspondence.start_space == start_space
                and correspondence.end_space == end_space
            ):
                return True
        return False

    def __repr__(self) -> str:
        inputs = ", ".join([space.structure_id for space in self.input_spaces])
        return (
            f"<{self.structure_id} from {inputs} to {self.output_space.structure_id}>"
        )
