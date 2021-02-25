from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Word


class WordSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        Selector.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.champion = champion
        self.challenger = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Word,
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
        champion = bubble_chamber.words.get_active()
        return cls.spawn(parent_id, bubble_chamber, champion, champion.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _passes_preliminary_checks(self):
        print("hello")
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        from homer.codelets.builders import WordBuilder

        self.child_codelets.append(
            WordBuilder.make(self.codelet_id, self.bubble_chamber)
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winner,
                self.follow_up_urgency,
            )
        )
