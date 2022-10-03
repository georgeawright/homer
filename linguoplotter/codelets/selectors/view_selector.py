from linguoplotter.codelets.selector import Selector
from linguoplotter.errors import MissingStructureError
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection_keys import exigency
from linguoplotter.structures import View
from linguoplotter.structure_collection_keys import activation


class ViewSelector(Selector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters import ViewSuggester

        return ViewSuggester

    @classmethod
    def get_follow_up_evaluator(cls) -> type:
        from linguoplotter.codelets.evaluators import ViewEvaluator

        return ViewEvaluator

    @classmethod
    def get_target_class(cls):
        return View

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            self._get_challenger()
        except MissingStructureError:
            return True
        return True

    def _engender_follow_up(self):
        # spawn a top-down view suggester with copy of winning view's frame
        winning_view = self.winners.get()
        if winning_view.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE:
            try:
                target_frame = winning_view.parent_frame.parent_concept.relatives.where(
                    is_frame=True
                ).get(key=exigency)
            except MissingStructureError:
                target_frame = winning_view.parent_frame
            self.child_codelets.append(
                self.get_follow_up_class().make(
                    self.codelet_id,
                    self.bubble_chamber,
                    frame=target_frame,
                )
            )
        self.child_codelets.append(
            self.get_follow_up_evaluator().spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )

    def _get_challenger(self):
        champion_view = self.champions.get()
        challenger_view = (
            self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept
                == champion_view.parent_frame.parent_concept
                and not champion_view.members.filter(
                    lambda c: c.start.parent_space in x.input_spaces
                ).is_empty()
                and not x.members.filter(
                    lambda c: c.start.parent_space in x.input_spaces
                ).is_empty()
                and x.raw_input_nodes() == champion_view.raw_input_nodes()
            )
            .excluding(champion_view)
            .get(key=activation)
        )
        self.challengers = self.bubble_chamber.new_structure_collection(challenger_view)

    def _fizzle(self):
        pass
