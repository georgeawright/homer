from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.evaluators import LabelEvaluator
from linguoplotter.codelets.suggesters import LabelSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import activation, labeling_exigency
from linguoplotter.structures.links import Label


class LabelSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_label = self._get_representative(self.champions)
        candidates = champion_label.start.labels_in_space(
            champion_label.parent_concept.parent_space
        )
        try:
            challenger_label = candidates.get(key=activation, exclude=[champion_label])
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_label
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, self.challengers, "Found challengers"
            )
            return True
        except MissingStructureError:
            return True

    def _get_representative(self, collection: StructureCollection):
        try:
            return collection.filter(lambda x: x.start.is_node).get()
        except MissingStructureError:
            representative = collection.get()
            while representative.start.is_label:
                representative = representative.start
            return representative

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        try:
            winning_label = self.winners.get()
            parent_concept = (
                winning_label.parent_concept.friends().where(structure_type=Label).get()
            )
            target_node = (
                winning_label.start.nearby()
                .where(is_slot=False)
                .get(key=labeling_exigency)
            )
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
            LabelEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
