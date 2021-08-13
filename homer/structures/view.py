from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
        members: StructureCollection,
        input_spaces: StructureCollection,
        output_space: WorkingSpace,
        quality: FloatBetweenOneAndZero,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations=[],
            quality=quality,
        )
        self.value = None
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.slot_values = {}
        self.is_view = True

    @property
    def raw_input_space(self) -> Space:
        return StructureCollection(
            {
                space
                for space in self.input_spaces
                if space.parent_concept.name == "input"
            }
        ).get()

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
        return StructureCollection.union(*[frame.slots for frame in self.input_frames])

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
