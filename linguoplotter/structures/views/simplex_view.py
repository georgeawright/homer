import statistics
from typing import List

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Frame
from linguoplotter.structures import Space, View
from linguoplotter.structures.spaces import ContextualSpace


class SimplexView(View):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        parent_frame: Frame,
        locations: List[Location],
        members: StructureCollection,
        frames: StructureCollection,
        input_spaces: StructureCollection,
        output_space: ContextualSpace,
        quality: FloatBetweenOneAndZero,
        prioritized_targets: StructureCollection,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        sub_views: StructureCollection,
        super_views: StructureCollection,
    ):
        View.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            parent_frame=parent_frame,
            locations=locations,
            members=members,
            frames=frames,
            input_spaces=input_spaces,
            output_space=output_space,
            quality=quality,
            prioritized_targets=prioritized_targets,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            sub_views=sub_views,
            super_views=super_views,
        )
        self.is_simplex_view = True

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators.view_evaluators import (
            SimplexViewEvaluator,
        )

        return SimplexViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors.view_selectors import SimplexViewSelector

        return SimplexViewSelector

    def nearby(self, space: Space = None) -> StructureCollection:
        def input_coords(view):
            return [
                coord
                for member in view.members
                for coord in member.start.location_in_space(
                    member.start_space
                ).coordinates
                if member.start_space.parent_concept.name == "input"
            ]

        def input_overlap(view_1, view_2):
            view_1_coords = input_coords(view_1)
            view_2_coords = input_coords(view_2)
            coords_in_both = [
                coord for coord in view_1_coords if coord in view_2_coords
            ]
            proportion_in_view_1 = len(coords_in_both) / len(view_1_coords)
            proportion_in_view_2 = len(coords_in_both) / len(view_2_coords)
            return statistics.fmean([proportion_in_view_1, proportion_in_view_2])

        space = space if space is not None else self.location.space
        return (
            space.contents.where(is_view=True)
            .filter(lambda x: input_overlap(x, self) > 0.5)
            .excluding(self)
        )

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount
        for member in self.members:
            member.decay_activation(amount)
        self.output_space.decay_activation(amount)
