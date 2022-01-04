import statistics
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Frame
from homer.structures import Space, View
from homer.structures.spaces import ContextualSpace


class SimplexView(View):
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
        self.is_simplex_view = True

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator

        return SimplexViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors.view_selectors import SimplexViewSelector

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

    def copy(self, **kwargs: dict):
        """Requires keyword arguments 'bubble_chamber', 'parent_id',
        'original_structure', and, 'replacement_structure'."""
        from homer.structures.links import Correspondence

        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        original_structure = kwargs["original_structure"]
        replacement_structure = kwargs["replacement_structure"]
        new_members = bubble_chamber.new_structure_collection()
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
        new_view = SimplexView(
            ID.new(SimplexView),
            parent_id,
            parent_frame=self.parent_frame,
            locations=self.locations,
            members=new_members,
            input_spaces=self.input_spaces,
            output_space=new_output_space,
            quality=self.quality,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=bubble_chamber.new_structure_collection(),
        )
        for correspondence in new_output_space.contents.of_type(Correspondence):
            new_view.members.add(correspondence)
        return new_view

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount
        for member in self.members:
            member.decay_activation(amount)
        self.output_space.decay_activation(amount)
