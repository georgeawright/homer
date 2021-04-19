from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures import View


class MonitoringView(View):
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
