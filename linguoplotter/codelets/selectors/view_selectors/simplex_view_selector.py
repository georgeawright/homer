from linguoplotter.codelets.selectors import ViewSelector
from linguoplotter.errors import MissingStructureError
from linguoplotter.structures.views import SimplexView
from linguoplotter.structure_collection_keys import activation


class SimplexViewSelector(ViewSelector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters.view_suggesters import (
            SimplexViewSuggester,
        )

        return SimplexViewSuggester

    @classmethod
    def get_follow_up_evaluator(cls) -> type:
        from linguoplotter.codelets.evaluators.view_evaluators import (
            SimplexViewEvaluator,
        )

        return SimplexViewEvaluator

    @classmethod
    def get_target_class(cls):
        return SimplexView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            self._get_challenger()
        except MissingStructureError:
            return True
        return True

    def _get_challenger(self):
        champion_view = self.champions.get()
        challenger_view = self.bubble_chamber.views.filter(
            lambda x: x.parent_frame.parent_concept
            == champion_view.parent_frame.parent_concept
            and not champion_view.members.filter(
                lambda c: c.start.parent_space in x.input_spaces
            ).is_empty()
            and not x.members.filter(
                lambda c: c.start.parent_space in x.input_spaces
            ).is_empty()
            and x.raw_input_nodes() == champion_view.raw_input_nodes()
        ).get(key=activation)
        self.challengers = self.bubble_chamber.new_structure_collection(challenger_view)
