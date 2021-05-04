from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import LabelBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class LabelSelector(Selector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.labels.get_active()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({champion}),
            champion.activation,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_label = self.champions.get_random()
        candidates = champion_label.start.labels_in_space(champion_label.parent_space)
        if len(candidates) == 1:
            return False
        try:
            challenger_label = candidates.get_active(exclude=[champion_label])
            self.challengers = StructureCollection({challenger_label})
            return True
        except MissingStructureError:
            return False

    def _fizzle(self):
        target = self.champions.get_random().start
        self.child_codelets.append(
            LabelBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                target,
                target.unhappiness,
            )
        )

    def _engender_follow_up(self):
        target_concept = self.champions.get_random().parent_concept
        self.child_codelets.append(
            LabelBuilder.make_top_down(
                self.codelet_id,
                self.bubble_chamber,
                target_concept,
            )
        )
        self.child_codelets.append(
            LabelSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
