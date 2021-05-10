from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.spaces import WorkingSpace


class DiscourseView(View):
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
        View.__init__(
            self,
            structure_id,
            parent_id,
            location,
            members,
            input_spaces,
            output_space,
            quality,
        )
        self.is_discourse_view = True

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders.view_builders import DiscourseViewBuilder

        return DiscourseViewBuilder

    def nearby(self, space: Space = None) -> StructureCollection:
        space = space if space is not None else self.location.space
        return StructureCollection(
            {
                view
                for view in space.contents.where(is_view=True)
                if view != self
                and not StructureCollection.intersection(
                    view.input_working_spaces, self.input_working_spaces
                ).is_empty()
            }
        )
