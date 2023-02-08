from linguoplotter.codelets.selector import Selector
from linguoplotter.errors import MissingStructureError
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Frame


class FrameSelector(Selector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters import FrameSuggester

        return FrameSuggester

    @classmethod
    def get_target_class(cls):
        return Frame

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["frame"]

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
            winning_frame = self.winners.get()
            if winning_frame.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE:
                target_frame = self.bubble_chamber.new_set(winning_frame.progenitor)
                self.child_codelets.append(
                    self.get_follow_up_class().make_top_down(
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
        view = self.bubble_chamber.views.filter(
            lambda x: champion in x.secondary_frames
        ).get()
        champion_correspondees = self.bubble_chamber.new_set(
            *[
                c.start
                for c in view.members
                if c.end in champion.input_space.contents
                or c.end in champion.output_space.contents
            ]
        )
        correspondences = StructureSet.union(
            *[
                c.correspondences
                for c in champion_correspondees
                if c.end not in champion.input_space.contents
                and c.end not in champion.output_space.contents
            ]
        )
        challenger_frame = (
            view.secondary_frames.excluding(champion)
            .filter(
                lambda x: any(
                    [
                        c.end in x.input_space or c.end in x.output_space
                        for c in correspondences
                    ]
                )
            )
            .get(key=activation)
        )
        self.challengers.add(challenger_frame)

    def _fizzle(self):
        pass
