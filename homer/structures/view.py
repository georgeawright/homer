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
        return StructureCollection(
            {
                structure
                for space in self.input_spaces
                for structure in space.contents
                if structure.is_slot
            }
        )

    def copy(self, **kwargs: dict):
        """Requires keyword arguments 'bubble_chamber', 'parent_id',
        'original_structure', and, 'replacement_structure'."""
        from homer.structures.links import Correspondence

        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        original_structure = kwargs["original_structure"]
        replacement_structure = kwargs["replacement_structure"]
        new_members = StructureCollection()
        for correspondence in self.members:
            if (
                correspondence.start in self.output_space.contents
                or correspondence.end in self.output_space.contents
            ):
                continue
            new_correspondence = correspondence.copy(
                old_arg=original_structure,
                new_arg=replacement_structure,
                parent_id=parent_id,
            )
            new_correspondence.start.links_in.add(new_correspondence)
            new_correspondence.start.links_out.add(new_correspondence)
            new_correspondence.end.links_in.add(new_correspondence)
            new_correspondence.end.links_out.add(new_correspondence)
            new_members.add(new_correspondence)
        new_output_space = self.output_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        new_view = View(
            ID.new(View),
            parent_id,
            location=self.location,
            members=new_members,
            input_spaces=self.input_spaces,
            output_space=new_output_space,
            quality=self.quality,
        )
        for correspondence in new_output_space.contents.of_type(Correspondence):
            new_view.members.add(correspondence)
        return new_view

    def nearby(self, space: Space = None) -> StructureCollection:
        space = space if space is not None else self.location.space
        return StructureCollection(
            {
                view
                for view in space.contents.of_type(View)
                if StructureCollection.intersection(
                    view.input_spaces, self.input_working_spaces
                )
                == self.input_working_spaces
                and view != self
            }
        )

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
