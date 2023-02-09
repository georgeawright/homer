from linguoplotter.codelets.selector import Selector
from linguoplotter.errors import MissingStructureError
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection_keys import activation, exigency
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import View


class ViewSelector(Selector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters import ViewSuggester

        return ViewSuggester

    @classmethod
    def get_target_class(cls):
        return View

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        try:
            self._get_challenger()
        except MissingStructureError:
            return True
        return True

    def _engender_follow_up(self):
        try:
            winning_view = self.winners.get()
            if winning_view.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE:
                target_frame = (
                    StructureSet.union(
                        self.bubble_chamber.new_set(winning_view.parent_frame),
                        winning_view.parent_frame.parent_concept.relatives.where(
                            is_frame=True, is_sub_frame=False, is_secondary=False
                        ),
                    )
                    .filter(
                        lambda f: self.bubble_chamber.views.filter(
                            lambda v: v.parent_frame.parent_concept == f.parent_concept
                            and v.members.is_empty
                        ).is_empty
                    )
                    .get(key=exigency)
                )
                self.child_codelets.append(
                    self.get_follow_up_class().make(
                        self.codelet_id,
                        self.bubble_chamber,
                        frame=target_frame,
                        urgency=target_frame.activation,
                    )
                )
        except MissingStructureError:
            pass

    def _get_challenger(self):
        champion = self.champions.get()
        self.challengers.add(
            self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept
                == champion.parent_frame.parent_concept
                and (
                    champion.members.filter(
                        lambda c: c.start.parent_space in x.input_spaces
                    ).not_empty
                    and x.members.filter(
                        lambda c: c.start.parent_space in champion.input_spaces
                    ).not_empty
                    and x.raw_input_nodes == champion.raw_input_nodes
                )
                or (any([x in sub_view.super_views for sub_view in champion.sub_views]))
            )
            .excluding(champion)
            .get(key=activation)
        )

    def _fizzle(self):
        pass
