from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.spaces import WorkingSpace


class DiscourseView(View):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        members: StructureCollection,
        input_spaces: StructureCollection,
        output_space: WorkingSpace,
        quality: FloatBetweenOneAndZero,
    ):
        View.__init__(
            self,
            structure_id,
            parent_id,
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

    def decay_activation(self, amount: float = None):
        if self.stable:
            return
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount
        for member in self.members:
            member.decay_activation(amount)
        self.output_space.decay_activation(amount)
