import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection


class Selector(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champions: StructureCollection,
        urgency: FloatBetweenOneAndZero,
        challengers: StructureCollection = None,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.champions = champions
        self.challengers = challengers
        self.winners = None
        self.losers = None
        self.confidence = 0.0
        self.follow_up_urgency = 0.0

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champions: StructureCollection,
        urgency: FloatBetweenOneAndZero,
        challengers: StructureCollection = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            champions,
            urgency,
            challengers=challengers,
        )

    def run(self) -> CodeletResult:
        self.bubble_chamber.loggers["activity"].log_champions(self)
        self.bubble_chamber.loggers["activity"].log_challengers(self)
        if not self._passes_preliminary_checks():
            self._fizzle()
            self._decay_activations()
            self.result = CodeletResult.FIZZLE
            return self.result
        if self.challengers is not None:
            self._hold_competition()
            self.bubble_chamber.loggers["activity"].log_winners(self)
            self.bubble_chamber.loggers["activity"].log_losers(self)
            self._boost_winners()
            self._decay_losers()
            for structure in StructureCollection.union(self.winners, self.losers):
                self.bubble_chamber.loggers["structure"].log(structure)
        else:
            self.winners = self.champions
            self.bubble_chamber.loggers["activity"].log_winners(self)
            self.confidence = self.winners.get().quality
            random_number = self.bubble_chamber.random_machine.generate_number()
            if self.confidence > random_number:
                self._boost_winners()
            for structure in self.winners:
                self.bubble_chamber.loggers["structure"].log(structure)
        self._boost_activations()
        self.follow_up_urgency = FloatBetweenOneAndZero(
            self.winners.get().quality - self.winners.get().activation
        )
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _hold_competition(self):
        champion_representative = self._get_representative(self.champions)
        challenger_representative = self._get_representative(self.challengers)
        champions_quality = champion_representative.quality
        self.bubble_chamber.loggers["activity"].log(
            self, f"Champion quality: {champions_quality}"
        )
        challengers_quality = challenger_representative.quality
        self.bubble_chamber.loggers["activity"].log(
            self, f"Challenger quality: {challengers_quality}"
        )
        champ_size_adjusted_quality = champions_quality * self._champions_size
        chall_size_adjusted_quality = challengers_quality * self._challengers_size
        total_quality = champ_size_adjusted_quality + chall_size_adjusted_quality
        try:
            champ_normalized_quality = champ_size_adjusted_quality / total_quality
        except ZeroDivisionError:
            champ_normalized_quality = 0.0
        choice = random.random()
        if choice < champ_normalized_quality:
            self.winners, self.losers = self.champions, self.challengers
            self.confidence = FloatBetweenOneAndZero(
                champ_size_adjusted_quality - chall_size_adjusted_quality
            )
        else:
            self.losers, self.winners = self.champions, self.challengers
            self.confidence = FloatBetweenOneAndZero(
                chall_size_adjusted_quality - champ_size_adjusted_quality
            )
        if self.challengers.get().activation > self.champions.get().activation:
            tmp = self.champions
            self.champions = self.challengers
            self.challengers = tmp

    @property
    def _parent_link(self):
        return self._structure_concept.relations_with(self._select_concept).get()

    @property
    def _select_concept(self):
        return self.bubble_chamber.concepts["select"]

    @property
    def _structure_concept(self):
        raise NotImplementedError

    @property
    def _champions_size(self):
        return self._get_representative(self.champions).size

    @property
    def _challengers_size(self):
        return self._get_representative(self.challengers).size

    def _boost_activations(self):
        self._select_concept.boost_activation(self.confidence)
        self._parent_link.boost_activation(self.confidence)
        self._select_concept.update_activation()
        self._parent_link.update_activation()

    def _decay_activations(self):
        self._select_concept.decay_activation()
        self._parent_link.decay_activation(1 - self.confidence)
        self._select_concept.update_activation()
        self._parent_link.update_activation()

    def _boost_winners(self):
        for winner in self.winners:
            winner.boost_activation(self.confidence)
            winner.update_activation()

    def _decay_losers(self):
        for loser in self.losers:
            loser.decay_activation(self.confidence)
            loser.update_activation()

    def _get_representative(self, collection: StructureCollection):
        return collection.get()

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        raise NotImplementedError
