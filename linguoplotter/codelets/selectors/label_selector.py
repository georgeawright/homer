from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.suggesters import LabelSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation, labeling_salience


class LabelSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        champion = self.champions.get()
        try:
            self.challengers.add(
                champion.start.champion_labels.filter(
                    lambda x: x.is_competing_with(champion)
                ).get()
            )
        except MissingStructureError:
            try:
                self.challengers.add(
                    champion.start.labels.filter(
                        lambda x: x.is_competing_with(champion)
                    ).get(key=activation)
                )
            except MissingStructureError:
                return True
        return True

    def _fizzle(self):
        pass

    def _rearrange_champions(self):
        winning_label = self.winners.get()
        start_node = winning_label.start
        start_node.champion_labels.add(winning_label)
        if self.losers.not_empty:
            losing_label = self.losers.get()
            start_node.champion_labels.remove(losing_label)

    def _engender_follow_up(self):
        try:
            winning_label = self.winners.get()
            parent_concept = winning_label.parent_concept
            new_start = (
                winning_label.start.nearby()
                .filter(lambda x: x.quality > 0)
                .get(key=labeling_salience)
            )
            targets = self.bubble_chamber.new_dict(
                {"start": new_start, "concept": parent_concept}, name="targets"
            )
            self.child_codelets.append(
                LabelSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    new_start.unlabeledness,
                )
            )
        except MissingStructureError:
            pass
