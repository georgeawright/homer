from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Link
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
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.slot_values = {}

    @classmethod
    def new(
        cls,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        members: StructureCollection = None,
    ):
        members = members if members is not None else StructureCollection()
        input_spaces = StructureCollection(
            set.union(
                *[
                    {
                        correspondence.start_space.location.space,
                        correspondence.end_space.location.space,
                    }
                    for correspondence in members
                ]
            )
        )
        view_id = ID.new(View)
        view_location = Location([], bubble_chamber.spaces["top level working"])
        view_output = WorkingSpace(
            ID.new(WorkingSpace),
            parent_id,
            f"output for {view_id}",
            bubble_chamber.concepts["text"],
            bubble_chamber.spaces["text"],
            [view_location],
            StructureCollection(),
            1,
            [],
            [],
        )
        view_location.space.add(view_output)
        bubble_chamber.working_spaces.add(view_output)
        view = View(
            view_id, parent_id, view_location, members, input_spaces, view_output, 0.0
        )
        view_location.space.add(view)
        bubble_chamber.views.add(view)
        return view

    @property
    def input_working_spaces(self):
        return StructureCollection(
            {space for space in self.input_spaces if not isinstance(space, Frame)}
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

    def copy(
        self,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        original_structure: Structure = None,
        replacement_structure: Structure = None,
    ):
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
        new_view = self.new(
            bubble_chamber=bubble_chamber, parent_id=parent_id, members=new_members
        )
        for structure in self.output_space.contents:
            if isinstance(structure, Link):
                continue
            structure_copy = structure.copy(
                bubble_chamber=bubble_chamber,
                parent_id=parent_id,
                parent_space=new_view.output_space,
            )
            new_view.output_space.add(structure_copy)
            for correspondence in structure.correspondences:
                new_correspondence = correspondence.copy(
                    old_arg=structure,
                    new_arg=structure_copy,
                    parent_id=parent_id,
                )
                new_correspondence.start.links_in.add(new_correspondence)
                new_correspondence.start.links_out.add(new_correspondence)
                new_correspondence.end.links_in.add(new_correspondence)
                new_correspondence.end.links_out.add(new_correspondence)
                new_view.members.add(new_correspondence)
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
