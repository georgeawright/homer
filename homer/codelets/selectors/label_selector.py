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
        try:
            challenger_label = candidates.get_active(exclude=[champion_label])
            self.challengers = StructureCollection({challenger_label})
            return True
        except MissingStructureError:
            return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        try:
            winning_label = self.winners.get_random()
            target_concept = winning_label.parent_concept.friends().get_random()
            target_node = winning_label.start.nearby().get_unhappy()
            self.child_codelets.append(
                LabelBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_node,
                    target_node.unlinkedness,
                    parent_concept=target_concept,
                )
            )
        except MissingStructureError:
            pass
        self.child_codelets.append(
            LabelSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
