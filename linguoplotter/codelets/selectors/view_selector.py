from linguoplotter.codelets.selector import Selector
from linguoplotter.errors import MissingStructureError
from linguoplotter.hyper_parameters import HyperParameters


class ViewSelector(Selector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_view = self.champions.get()
            challenger_view = champion_view.nearby().get()
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_view
            )
        except MissingStructureError:
            return True
        return True

    def _engender_follow_up(self):
        # spawn a top-down view suggester with copy of winning view's frame
        winning_view = self.winners.get()
        if winning_view.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE:
            self.child_codelets.append(
                self.get_follow_up_class().make(
                    self.codelet_id,
                    self.bubble_chamber,
                    frame=winning_view.parent_frame,
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

    def _fizzle(self):
        pass
