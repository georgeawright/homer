from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk
from homer.structures.links.correspondence import Correspondence
from homer.structures.space import Space
from homer.structures.spaces import WorkingSpace


class View(Chunk):
    """A chunk of self-consistent correspondences."""

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
        value = None
        parent_space = location.space
        Chunk.__init__(
            self,
            structure_id,
            parent_id,
            value,
            [location],
            members,
            parent_space,
            quality,
            StructureCollection({parent_space}),
        )
        self.input_spaces = input_spaces
        self.output_space = output_space

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
                    {correspondence.start_space, correspondence.end_space}
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
            view_location,
            StructureCollection(),
            1,
            [],
            [],
        )
        bubble_chamber.working_spaces.add(view_output)
        view = View(
            view_id, parent_id, view_location, members, input_spaces, view_output, 0.0
        )
        bubble_chamber.views.add(view)
        return view

    @property
    def size(self):
        return len(self.members)
