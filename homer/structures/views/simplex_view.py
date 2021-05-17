from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.spaces import WorkingSpace


class SimplexView(View):
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
        new_view = SimplexView(
            ID.new(SimplexView),
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

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount
        for member in self.members:
            member.decay_activation(amount)
        self.output_space.decay_activation(amount)
