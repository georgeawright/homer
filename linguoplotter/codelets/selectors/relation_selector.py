from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.evaluators import RelationEvaluator
from linguoplotter.codelets.suggesters import RelationSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import activation


class RelationSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_relation = self.champions.get()
        try:
            challenger_relation = (
                champion_relation.start.champion_relations.filter(
                    lambda x: x.end == champion_relation.end
                    and x.conceptual_space == champion_relation.conceptual_space
                    and x.parent_concept.parent_space == champion_relation.parent_space
                )
                .excluding(champion_relation)
                .get()
            )
        except MissingStructureError:
            try:
                challenger_relation = (
                    champion_relation.start.relations.filter(
                        lambda x: x.end == champion_relation.end
                        and x.conceptual_space == champion_relation.conceptual_space
                        and x.parent_concept.parent_space
                        == champion_relation.parent_space
                    )
                    .excluding(champion_relation)
                    .get(key=activation)
                )
            except MissingStructureError:
                return True
        self.challengers = self.bubble_chamber.new_structure_collection(
            challenger_relation
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, self.challengers, "Found challengers"
        )
        return True

    def _fizzle(self):
        pass

    def _rearrange_champions(self):
        winning_relation = self.winners.get()
        start_node = winning_relation.start
        end_node = winning_relation.end
        start_node.champion_relations.add(winning_relation)
        end_node.champion_relations.add(winning_relation)
        if self.losers is not None:
            losing_relation = self.losers.get()
            start_node.champion_relations.remove(losing_relation)
            end_node.champion_relations.remove(losing_relation)

    def _engender_follow_up(self):
        try:
            winner_relation = self.winners.get()
            parent_concept = winner_relation.parent_concept.friends().get()
            target_space = StructureCollection.intersection(
                winner_relation.start.parent_spaces.where(no_of_dimensions=1),
                winner_relation.end.parent_spaces.where(no_of_dimensions=1),
            ).get(exclude=[winner_relation.conceptual_space])
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
