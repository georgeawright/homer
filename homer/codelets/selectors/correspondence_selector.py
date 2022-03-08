from homer.codelets.selector import Selector
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.errors import MissingStructureError
from homer.structure_collection_keys import activation, corresponding_exigency


class CorrespondenceSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_correspondence = self.champions.where(is_correspondence=True).get()
        candidates = champion_correspondence.nearby()
        try:
            challenger_correspondence = candidates.get(
                key=activation, exclude=[champion_correspondence]
            )
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_correspondence
            )
        except MissingStructureError:
            pass
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        from homer.codelets.suggesters.correspondence_suggesters import (
            SpaceToFrameCorrespondenceSuggester,
            SubFrameToFrameCorrespondenceSuggester,
        )

        self.child_codelets.append(
            CorrespondenceEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
        winner_correspondence = self.winners.where(is_correspondence=True).get()
        target_view = winner_correspondence.parent_view
        try:
            target_space_two = winner_correspondence.end.parent_space
            target_structure_two = target_space_two.contents.where(
                is_correspondence=False
            ).get(key=corresponding_exigency)
            parent_concept = winner_correspondence.parent_concept.friends().get()
        except MissingStructureError:
            return
        follow_up_class = SubFrameToFrameCorrespondenceSuggester
        for input_space in target_view.input_spaces:
            if winner_correspondence.start in input_space.contents:
                follow_up_class = SpaceToFrameCorrespondenceSuggester
                break
        self.child_codelets.append(
            follow_up_class.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_view": target_view,
                    "target_space_two": target_space_two,
                    "target_structure_two": target_structure_two,
                    "parent_concept": parent_concept,
                },
                target_view.exigency,
            )
        )
