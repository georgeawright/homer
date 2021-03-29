from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import LabelBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure


class LabelSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Structure,
        urgency: FloatBetweenOneAndZero,
        challenger: Structure = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Structure,
        urgency: FloatBetweenOneAndZero,
        challenger: Structure = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            champion,
            urgency,
            challenger=challenger,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.labels.get_active()
        return cls.spawn(parent_id, bubble_chamber, champion, champion.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        candidates = self.champion.start.labels_in_space(self.champion.parent_space)
        if len(candidates) == 1:
            return False
        try:
            self.challenger = candidates.get_active(exclude=[self.champion])
            return True
        except MissingStructureError:
            return False

    def _fizzle(self):
        self.child_codelets.append(
            LabelBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.champion.start,
                self.champion.start.unhappiness,
            )
        )

    def _engender_follow_up(self):
        new_target = self.bubble_chamber.input_nodes.get_exigent()
        self.child_codelets.append(
            LabelBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                new_target.unlinkedness,
                parent_concept=self.champion.parent_concept,
            )
        )
        self.child_codelets.append(
            LabelSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winner,
                self.follow_up_urgency,
                challenger=self.loser,
            )
        )
