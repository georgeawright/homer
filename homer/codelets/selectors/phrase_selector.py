from homer.bubble_chamber import BubbleChamber
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class PhraseSelector(Selector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.phrases.get_active()
        return cls.spawn(parent_id, bubble_chamber, champion, champion.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["phrase"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_phrase = self.champions.get_random()
            challenger_phrase = champion_phrase.nearby().get_active()
            self.challengers = StructureCollection({challenger_phrase})
        except MissingStructureError:
            return True
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        from homer.codelets.builders import PhraseBuilder

        self.child_codelets.append(
            PhraseBuilder.make(self.codelet_id, self.bubble_chamber)
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
