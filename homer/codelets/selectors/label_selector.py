from homer.codelets.selector import Selector
from homer.codelets.suggesters import LabelSuggester
from homer.errors import MissingStructureError
from homer.structure_collection_keys import activation, labeling_exigency


class LabelSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_label = self.champions.get()
        candidates = champion_label.start.labels_in_space(champion_label.parent_space)
        try:
            challenger_label = candidates.get(key=activation, exclude=[champion_label])
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_label
            )
            return True
        except MissingStructureError:
            return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        try:
            winning_label = self.winners.get()
            parent_concept = winning_label.parent_concept.friends().get()
            target_node = winning_label.start.nearby().get(key=labeling_exigency)
            self.child_codelets.append(
                LabelSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    {"target_node": target_node, "parent_concept": parent_concept},
                    target_node.unlabeledness,
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
