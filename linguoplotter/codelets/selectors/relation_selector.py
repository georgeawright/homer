from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.suggesters import RelationSuggester
from linguoplotter.errors import MissingStructureError


class RelationSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        """
        Champions are relations in a single conceptual space which have the same arguments
        and the same or reverse concepts
        (eg: {less-time(x,y), more-time(y,x)}
             {different-location(x,y), different-location(y,x)})
        Challengers are:
        - Relations with same arguments, in the same conceptual space or a competing conceptual space
          (eg north-south vs east-west, different-north-south vs less-north-south)
        """
        self._assemble_supporting_champions()
        if self.challengers.not_empty:
            return True
        self._get_challengers_with_same_or_competing_conceptual_space()
        return True

    def _assemble_supporting_champions(self):
        champion = self.champions.get()
        for relation in champion.start.relations.filter(
            lambda x: x not in self.champions and x.is_mutually_supportive_of(champion)
        ):
            self.champions.add(relation)

    def _get_challengers_with_same_or_competing_conceptual_space(self):
        champion = self.champions.get()
        challengers = champion.start.champion_relations.filter(
            lambda x: x.is_competing_with(champion)
        )
        if challengers.is_empty:
            try:
                challenger = champion.start.relations.filter(
                    lambda x: x.is_competing_with(champion)
                ).get(key=lambda x: x.quality)
                challengers = champion.start.relations.filter(
                    lambda x: x.start == challenger.end
                    and x.end == challenger.start
                    and x.conceptual_space == challenger.conceptual_space
                    and x.parent_concept == challenger.parent_concept.reverse
                )
            except MissingStructureError:
                pass
        for relation in challengers:
            self.challengers.add(relation)

    def _fizzle(self):
        pass

    def _rearrange_champions(self):
        self.bubble_chamber.loggers["activity"].log("Rearranging Champions")
        for winner in self.winners:
            winner.start.champion_relations.add(winner)
            winner.end.champion_relations.add(winner)
        for loser in self.losers:
            loser.start.champion_relations.remove(loser)
            loser.end.champion_relations.remove(loser)

    def _engender_follow_up(self):
        try:
            winner_relation = self.winners.get()
            self.child_codelets.append(
                RelationSuggester.make_top_down(
                    self.codelet_id,
                    self.bubble_chamber,
                    parent_concept=winner_relation.parent_concept,
                    conceptual_space=winner_relation.conceptual_space,
                    urgency=winner_relation.quality,
                )
            )
        except MissingStructureError:
            pass

    @property
    def _champions_size(self):
        """
        Counting parent concepts means more(x,y)+less(y,x)
        is preferred to different(x,y)+different(y,x)
        """
        return len({relation.parent_concept: True for relation in self.champions})

    @property
    def _challengers_size(self):
        return len({relation.parent_concept: True for relation in self.challengers})
