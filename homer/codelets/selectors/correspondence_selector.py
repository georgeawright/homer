from homer.codelets.selector import Selector
from homer.codelets.suggesters import CorrespondenceSuggester
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
        winner_correspondence = self.winners.where(is_correspondence=True).get()
        target_view = winner_correspondence.parent_view
        try:
            target_structure_one = (
                winner_correspondence.start.nearby().get(key=corresponding_exigency)
                if winner_correspondence.start.is_node
                else (
                    winner_correspondence.start.arguments.get()
                    .links.where(is_correspondence=False)
                    .get(
                        key=corresponding_exigency,
                        exclude=[winner_correspondence.start],
                    )
                )
            )
            target_space_one = target_structure_one.parent_space
            target_conceptual_space = target_structure_one.parent_spaces.where(
                is_conceptual_space=True, is_basic_level=True
            ).get()
            target_space_two = target_view.input_spaces.get(exclude=[target_space_one])
            target_structure_two = (
                None
                if winner_correspondence.start.is_node
                else (
                    self.bubble_chamber.new_structure_collection(
                        *[
                            structure
                            for structure in winner_correspondence.end.arguments.get()
                            .links.of_type(type(target_structure_one))
                            .where(parent_space=target_space_two)
                            if structure in target_conceptual_space.contents
                        ]
                    ).get(key=corresponding_exigency)
                )
            )
            target_concept = winner_correspondence.parent_concept.friends().get()
        except MissingStructureError:
            return
        self.child_codelets.append(
            CorrespondenceSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_view": winner_correspondence.parent_view,
                    "target_space_one": target_space_one,
                    "target_structure_one": target_structure_one,
                    "target_space_two": target_space_two,
                    "target_structure_two": target_structure_two,
                    "target_conceptual_space": target_conceptual_space,
                    "parent_concept": target_concept,
                },
                target_structure_one.uncorrespondedness,
            )
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
