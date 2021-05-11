from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
