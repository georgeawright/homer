from homer.bubble_chamber import BubbleChamber
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Phrase


class PhraseSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Phrase,
        urgency: FloatBetweenOneAndZero,
        challenger: Phrase = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Phrase,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            champion,
            urgency,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.phrases.get_active()
        return cls.spawn(parent_id, bubble_chamber, champion, champion.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["phrase"]

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        try:
            self.challenger = self.champion.nearby().get_active()
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
                self.winner,
                self.follow_up_urgency,
            )
        )
