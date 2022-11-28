import random

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureSet


class Selector(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champions: StructureSet,
        urgency: FloatBetweenOneAndZero,
        challengers: StructureSet = None,
    ):
        Codelet.__init__(
            self, codelet_id, parent_id, bubble_chamber, champions, urgency
        )
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
        champions: StructureSet,
        urgency: FloatBetweenOneAndZero,
        challengers: StructureSet = None,
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
        if self.challengers is None:
            self.challengers = self.bubble_chamber.new_set(name="challengers")
        self.winners = self.bubble_chamber.new_set(name="winners")
        self.losers = self.bubble_chamber.new_set(name="losers")
        self.bubble_chamber.loggers["activity"].log_set(self.champions)
        self.bubble_chamber.loggers["activity"].log_set(self.challengers)
        if not self._passes_preliminary_checks():
            self._fizzle()
            self._decay_activations()
            self.result = CodeletResult.FIZZLE
            return self.result
        if self.challengers.not_empty:
            self._hold_competition()
            self.bubble_chamber.loggers["activity"].log_set(self.winners)
            self.bubble_chamber.loggers["activity"].log_set(self.losers)
            self._boost_winners()
            self._decay_losers()
            for structure in StructureSet.union(self.winners, self.losers):
                self.bubble_chamber.loggers["structure"].log(structure)
        else:
            self.confidence = self.champions.get().quality
            if self.confidence == 0.0:
                for champion in self.champions:
                    self.losers.add(champion)
                self.bubble_chamber.loggers["activity"].log_set(self.losers)
                self._decay_losers()
                for structure in self.losers:
                    self.bubble_chamber.loggers["structure"].log(structure)
            else:
                for champion in self.champions:
                    self.winners.add(champion)
                self.bubble_chamber.loggers["activity"].log_set(self.winners)
                random_number = self.bubble_chamber.random_machine.generate_number()
                if self.confidence > random_number:
                    self._boost_winners()
                for structure in self.winners:
                    self.bubble_chamber.loggers["structure"].log(structure)
                self._rearrange_champions()
        self._boost_activations()
        try:
            self.follow_up_urgency = FloatBetweenOneAndZero(
                self.winners.get().quality - self.winners.get().activation
            )
        except MissingStructureError:
            self.follow_up_urgency = 0.0
        self._engender_follow_up()
        self.result = CodeletResult.FINISH
        return self.result

    def _hold_competition(self):
        champion_representative = self._get_representative(self.champions)
        challenger_representative = self._get_representative(self.challengers)
        champions_quality = champion_representative.quality
        self.bubble_chamber.loggers["activity"].log(
            f"Champion quality: {champions_quality}"
        )
        challengers_quality = challenger_representative.quality
        self.bubble_chamber.loggers["activity"].log(
            f"Challenger quality: {challengers_quality}"
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
            if winner.quality > 0.0:
                winner.activate()
                if winner.is_link:
                    winner.parent_concept.boost_activation(self.confidence)
                elif winner.is_view:
                    winner.parent_frame.boost_activation(self.confidence)
            else:
                winner.deactivate()

    def _decay_losers(self):
        for loser in self.losers:
            loser.deactivate()
            if loser.is_link:
                loser.parent_concept.decay_activation(self.confidence)
            if loser.is_view:
                loser.parent_frame.decay_activation(self.confidence)

    def _rearrange_champions(self):
        pass

    def _get_representative(self, collection: StructureSet):
        return collection.get()

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        raise NotImplementedError
