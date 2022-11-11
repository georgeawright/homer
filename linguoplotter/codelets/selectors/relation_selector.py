from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.suggesters import RelationSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet


class RelationSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion = self.champions.get()
        try:
            self.challengers.add(
                champion.start.champion_relations.filter(
                    lambda x: x.end == champion.end
                    and x.conceptual_space == champion.conceptual_space
                )
                .excluding(champion)
                .get()
            )
        except MissingStructureError:
            try:
                self.challengers.add(
                    champion.start.relations.filter(
                        lambda x: x.end == champion.end
                        and x.conceptual_space == champion.conceptual_space
                    )
                    .excluding(champion)
                    .get(key=activation)
                )
            except MissingStructureError:
                try:
                    challenger = (
                        StructureSet.union(
                            champion.start.relations.filter(
                                lambda x: x.conceptual_space
                                == champion.conceptual_space
                            ),
                            champion.end.relations.filter(
                                lambda x: x.conceptual_space
                                == champion.conceptual_space
                            ),
                        )
                        .excluding(champion)
                        .get(key=activation)
                    )
                    self.challengers.add(challenger)
                    for relation in challenger.start.relations.filter(
                        lambda x: x.end == challenger.end
                        and x.conceptual_space
                        and x.activation > 0
                    ):
                        self.challengers.add(relation)
                    for relation in champion.start.relations.filter(
                        lambda x: x.end == challenger.end
                        and x.conceptual_space
                        and x.activation > 0
                    ):
                        self.champions.add(relation)
                except MissingStructureError:
                    return True
        return True

    def _fizzle(self):
        pass

    def _rearrange_champions(self):
        winning_relation = self.winners.get()
        start_node = winning_relation.start
        end_node = winning_relation.end
        start_node.champion_relations.add(winning_relation)
        end_node.champion_relations.add(winning_relation)
        if self.losers.not_empty:
            losing_relation = self.losers.get()
            start_node.champion_relations.remove(losing_relation)
            end_node.champion_relations.remove(losing_relation)

    def _engender_follow_up(self):
        try:
            winner_relation = self.winners.get()
            parent_concept = winner_relation.parent_concept
            target_space = StructureSet.intersection(
                # parent spaces doesn't contain the unidimensional location spaces
                winner_relation.start.parent_spaces.where(no_of_dimensions=1),
                winner_relation.end.parent_spaces.where(no_of_dimensions=1),
            ).get(exclude=[winner_relation.conceptual_space])
            targets = self.bubble_chamber.new_dict(
                {
                    "start": winner_relation.start,
                    "end": winner_relation.end,
                    "space": target_space,
                    "concept": parent_concept,
                },
                name="targets",
            )
            self.child_codelets.append(
                RelationSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    winner_relation.start.unrelatedness,
                )
            )
        except MissingStructureError:
            pass

    @property
    def _champions_size(self):
        return len(self.champions)

    @property
    def _challengers_size(self):
        return len(self.challengers)
