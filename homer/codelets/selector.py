import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class Selector(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.champion = None
        self.challenger = None
        self.winner = None
        self.loser = None
        self.confidence = 0.0
        self.follow_up_urgency = 0.0

    @classmethod
    def spawn(cls):
        raise NotImplementedError

    def run(self) -> CodeletResult:
        if not self._passes_preliminary_checks():
            self._fizzle()
            self._decay_activations()
            self.result = CodeletResult.FIZZLE
            return self.result
        if self.challenger is not None:
            self._hold_competition()
            self._boost_winner()
            self._decay_loser()
        else:
            self.winner = self.champion
            self.confidence = self.winner.quality
            self._boost_champion()
        self._boost_activations()
        self.follow_up_urgency = self.winner.quality - self.winner.activation
        self._engender_follow_up()
        self.result = CodeletResult.SUCCESS
        return self.result

    def _hold_competition(self):
        champ_size_adjusted_quality = self.champion.quality * self.champion.size
        chall_size_adjusted_quality = self.challenger.quality * self.challenger.size
        total_quality = champ_size_adjusted_quality + chall_size_adjusted_quality
        try:
            champ_normalized_quality = champ_size_adjusted_quality / total_quality
        except ZeroDivisionError:
            champ_normalized_quality = 0.0
        choice = random.random()
        if choice < champ_normalized_quality:
            self.winner, self.loser = self.champion, self.challenger
            self.confidence = FloatBetweenOneAndZero(
                champ_size_adjusted_quality - chall_size_adjusted_quality
            )
        else:
            self.loser, self.winner = self.champion, self.challenger
            self.confidence = FloatBetweenOneAndZero(
                chall_size_adjusted_quality - champ_size_adjusted_quality
            )
        if self.challenger.activation > self.champion.activation:
            tmp = self.champion
            self.champion = self.challenger
            self.challenger = tmp

    @property
    def _parent_link(self):
        return self._structure_concept.relations_with(self._select_concept).get_random()

    @property
    def _select_concept(self):
        return self.bubble_chamber.concepts["select"]

    @property
    def _structure_concept(self):
        raise NotImplementedError

    def _boost_activations(self):
        self._select_concept.boost_activation(self.confidence)
        self._parent_link.boost_activation(self.confidence)

    def _decay_activations(self):
        self._select_concept.decay_activation()
        self._parent_link.decay_activation(1 - self.confidence)

    def _boost_winner(self):
        self.winner.boost_activation(self.confidence)

    def _decay_loser(self):
        self.loser.decay_activation(self.confidence)

    def _boost_champion(self):
        self.champion.boost_activation(self.confidence)

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        raise NotImplementedError
