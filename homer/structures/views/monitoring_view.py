from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Frame, Space, View
from homer.structures.spaces import ContextualSpace


class MonitoringView(View):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        parent_frame: Frame,
        locations: List[Location],
        members: StructureCollection,
        input_spaces: StructureCollection,
        output_space: ContextualSpace,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
    ):
        View.__init__(
            self,
            structure_id,
            parent_id,
            parent_frame,
            locations,
            members,
            input_spaces,
            output_space,
            quality,
            links_in,
            links_out,
            parent_spaces,
        )
        self.is_monitoring_view = True

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders.view_builders import MonitoringViewBuilder

        return MonitoringViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator

        return MonitoringViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors.view_selectors import MonitoringViewSelector

        return MonitoringViewSelector

    @property
    def raw_input_in_view(self) -> StructureCollection:
        return StructureCollection.union(
            argument.raw_members
            for correspondence in self.members
            for argument in correspondence.end.arguments
        )

    def nearby(self, space: Space = None) -> StructureCollection:
        space = space if space is not None else self.location.space
        return (
            space.contents.where(is_view=True)
            .filter(
                lambda x: len(
                    StructureCollection.intersection(
                        self.raw_input_in_view, x.raw_input_in_view
                    )
                )
                > len(self.raw_input_in_view) * 0.5
                or len(
                    StructureCollection.intersection(
                        self.raw_input_in_view, x.raw_input_in_view
                    )
                )
                > len(x.raw_input_in_view) * 0.5
            )
            .excluding(self)
        )

    def decay_activation(self, amount: float = None):
        if self.stable:
            return
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount
        for member in self.members:
            member.decay_activation(amount)
