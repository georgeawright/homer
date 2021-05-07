from homer.structure_collection import StructureCollection
from homer.structures import Space, View


class DiscourseView(View):
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
