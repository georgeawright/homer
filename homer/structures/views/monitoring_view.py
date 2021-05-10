from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.spaces import WorkingSpace


class MonitoringView(View):
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
    def raw_input_space(self) -> Space:
        return StructureCollection(
            {
                space
                for space in self.input_spaces
                if space.parent_concept.name == "input"
            }
        ).get_random()

    @property
    def text_space(self) -> Space:
        return StructureCollection(
            {
                space
                for space in self.input_spaces
                if space.parent_concept.name == "text"
            }
        ).get_random()

    @property
    def interpretation_space(self) -> Space:
        return StructureCollection(
            {
                space
                for space in self.input_spaces
                if space.parent_concept.name == "interpretation"
            }
        ).get_random()

    @property
    def raw_input_in_view(self) -> StructureCollection:
        return StructureCollection.union(
            *[
                correspondence.arguments.where(is_raw=True)
                for correspondence in self.members
            ]
        )

    def nearby(self, space: Space = None) -> StructureCollection:
        space = space if space is not None else self.location.space
        return StructureCollection(
            {
                view
                for view in space.contents.of_type(View)
                if view != self
                and (
                    len(
                        StructureCollection.intersection(
                            self.raw_input_in_view, view.raw_input_in_view
                        )
                    )
                    > len(self.raw_input_in_view) * 0.5
                    or len(
                        StructureCollection.intersection(
                            self.raw_input_in_view, view.raw_input_in_view
                        )
                    )
                    > len(view.raw_input_in_view) * 0.5
                )
            }
        )
