from homer.codelets.selector import Selector
from homer.codelets.suggesters import RelationSuggester
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class RelationSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_relation = self.champions.get()
        space = champion_relation.conceptual_space
        candidates = champion_relation.start.relations_in_space_with(
            space, champion_relation.end
        )
        if len(candidates) > 1:
            challenger_relation = candidates.get(
                key=activation, exclude=[champion_relation]
            )
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_relation
            )
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        winner_relation = self.winners.get()
        parent_concept = winner_relation.parent_concept.friends().get()
        try:
            target_space = StructureCollection.intersection(
                winner_relation.start.parent_spaces.where(no_of_dimensions=1),
                winner_relation.end.parent_spaces.where(no_of_dimensions=1),
            ).get(exclude=[winner_relation.parent_space])
            self.child_codelets.append(
                RelationSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    {
                        "target_space": target_space,
                        "target_structure_one": winner_relation.start,
                        "target_structure_two": winner_relation.end,
                        "parent_concept": parent_concept,
                    },
                    winner_relation.start.unrelatedness,
                )
            )
        except MissingStructureError:
            pass
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
