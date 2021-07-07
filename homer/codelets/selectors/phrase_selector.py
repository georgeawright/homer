import statistics

from homer.codelets.selector import Selector
from homer.codelets.suggesters import PhraseSuggester
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, unchunkedness


class PhraseSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["phrase"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_phrase = self.champions.get()
            challenger_phrase = champion_phrase.nearby().get(key=activation)
            self.challengers = StructureCollection({challenger_phrase})
        except MissingStructureError:
            return True
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        try:
            winning_phrase = self.winners.get()
            text_space = winning_phrase.parent_space
            text_fragments = StructureCollection.union(
                text_space.contents.where(is_phrase=True),
                text_space.contents.where(is_word=True),
            )
            target_one = text_fragments.get(key=unchunkedness)
            target_two = target_one.potential_rule_mates.get(key=unchunkedness)
            try:
                target_three = StructureCollection.intersection(
                    target_one.potential_rule_mates, target_two.potential_rule_mates
                ).get(key=unchunkedness)
                targets = StructureCollection({target_one, target_two, target_three})
            except MissingStructureError:
                targets = StructureCollection({target_one, target_two})
            root, left_branch, right_branch = PhraseSuggester.arrange_targets(targets)
            urgency = statistics.fmean([target.unchunkedness for target in targets])
            self.child_codelets.append(
                PhraseSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    {
                        "target_root": root,
                        "target_left_branch": left_branch,
                        "target_right_branch": right_branch,
                        "target_rule": None,
                    },
                    urgency,
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
