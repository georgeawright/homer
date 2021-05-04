from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders.relation_builders import RelationProjectionBuilder
from homer.codelets.selectors import RelationSelector


class RelationProjectionSelector(RelationSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        self.child_codelets.append(
            RelationProjectionBuilder.make(
                self.codelet_id,
                self.bubble_chamber,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
