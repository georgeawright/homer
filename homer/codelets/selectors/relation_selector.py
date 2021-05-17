from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import RelationBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class RelationSelector(Selector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.relations.get_active()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({champion}),
            champion.activation,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_relation = self.champions.get_random()
        space = champion_relation.parent_space
        candidates = champion_relation.start.relations_in_space_with(
            space, champion_relation.end
        )
        if len(candidates) == 1:
            return False
        try:
            challenger_relation = candidates.get_active(exclude=[champion_relation])
            self.challengers = StructureCollection({challenger_relation})
            return True
        except MissingStructureError:
            return False

    def _fizzle(self):
        champion_relation = self.champions.get_random()
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                champion_relation.parent_spaces.get_random(),
                champion_relation.start,
                champion_relation.start.unhappiness,
            )
        )

    def _engender_follow_up(self):
        winner_relation = self.winners.get_random()
        target_concept = winner_relation.parent_concept.friends().get_random()
        try:
            target_space = StructureCollection.intersection(
                winner_relation.start.parent_spaces.where(no_of_dimensions=1),
                winner_relation.end.parent_spaces.where(no_of_dimensions=1),
            ).get_random(exclude=[winner_relation.parent_space])
            self.child_codelets.append(
                RelationBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_space,
                    winner_relation.start,
                    winner_relation.unlinkedness,
                    target_structure_two=winner_relation.end,
                    parent_concept=target_concept,
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
