import statistics
from typing import List, Union

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Chunk, Concept, Phrase, Rule, Word


class PhraseSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_rule = None
        self.target_root = None
        self.target_left_branch = None
        self.target_right_branch = None
        self.parent_space = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import PhraseBuilder

        return PhraseBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["target_rule"] is not None else "BottomUp"
        )
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get_active()
        target_one = target_view.output_space.contents.where(is_word=True).get_unhappy()
        target_two = target_one.potential_rule_mates.get_unhappy()
        try:
            target_three = StructureCollection.intersection(
                target_one.potential_rule_mates, target_two.potential_rule_mates
            ).get_unhappy()
            targets = StructureCollection({target_one, target_two, target_three})
        except MissingStructureError:
            targets = StructureCollection({target_one, target_two})
        root, left_branch, right_branch = cls.arrange_targets(targets)
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([target.unhappiness for target in targets])
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_root": root,
                "target_left_branch": left_branch,
                "target_right_branch": right_branch,
                "target_rule": None,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_rule: Rule,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_one = StructureCollection(
            {
                fragment
                for fragment in bubble_chamber.text_fragments
                if target_rule.is_compatible_with(fragment)
            }
        ).get_unhappy()
        target_two = StructureCollection(
            {
                fragment
                for fragment in target_one.potential_rule_mates
                if target_rule.is_compatible_with(target_one, fragment)
            }
        ).get_unhappy()
        try:
            target_three = StructureCollection(
                {
                    fragment
                    for fragment in StructureCollection.intersection(
                        target_one.potential_rule_mates, target_two.potential_rule_mates
                    )
                    if target_rule.is_compatible_with(target_one, target_two, fragment)
                }
            ).get_unhappy()
            targets = StructureCollection({target_one, target_two, target_three})
        except MissingStructureError:
            targets = StructureCollection({target_one, target_two})
        root, left_branch, right_branch = cls.arrange_targets(targets)
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([target.unhappiness for target in targets])
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_root": root,
                "target_left_branch": left_branch,
                "target_right_branch": right_branch,
                "target_rule": target_rule,
            },
            urgency,
        )

    @classmethod
    def arrange_targets(cls, targets: StructureCollection):
        root = None
        for target in targets:
            remaining_targets = StructureCollection.difference(
                targets, StructureCollection({target})
            )
            if hasattr(target, "members") and target.members == remaining_targets:
                root = target
                left_branch = root.left_branch
                right_branch = root.right_branch
        if root is None:
            branch_one = targets.get_random()
            branch_two = targets.get_random(exclude=[branch_one])
            if (
                branch_one.location.coordinates[0][0]
                < branch_two.location.coordinates[0][0]
            ):
                left_branch = branch_one
                right_branch = branch_two
            else:
                left_branch = branch_two
                right_branch = branch_one
        return (root, left_branch, right_branch)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["phrase"]

    @property
    def target_structures(self):
        targets = [
            self.target_root,
            self.target_left_branch,
            self.target_right_branch,
        ]
        return StructureCollection({target for target in targets if target is not None})

    def _passes_preliminary_checks(self):
        self.target_root = self._target_structures["target_root"]
        self.target_left_branch = self._target_structures["target_left_branch"]
        self.target_right_branch = self._target_structures["target_right_branch"]
        self.target_rule = self._target_structures["target_rule"]
        self.parent_space = self.target_structures.get_random().parent_space
        if len(self.target_structures) < 2:
            return False
        if self.target_rule is None:
            try:
                self.target_rule = StructureCollection(
                    {
                        rule
                        for rule in self.bubble_chamber.rules
                        if self._rule_is_compatible_with_targets(rule)
                    }
                ).get_random()
                self._target_structures["target_rule"] = self.target_rule
            except MissingStructureError:
                return False
        elif not self._rule_is_compatible_with_targets(self.target_rule):
            return False
        if len(self.target_structures) == 3:
            return any([target.is_slot for target in self.target_structures])
        for phrase in self.bubble_chamber.phrases:
            if (
                phrase.rule == self.target_rule
                and phrase.left_branch == self.target_left_branch
                and phrase.right_branch == self.target_right_branch
            ):
                return False
        return True

    def _calculate_confidence(self):
        mean_quality = statistics.fmean(
            [target.quality for target in self.target_structures if not target.is_slot]
        )
        self.confidence = mean_quality * self.target_rule.activation

    def _fizzle(self):
        pass

    def _rule_is_compatible_with_targets(self, rule: Concept):
        if self.target_left_branch is not None:
            left_branch_concepts = (
                StructureCollection({self.target_left_branch.parent_concept})
                if not isinstance(self.target_left_branch, Word)
                else StructureCollection(
                    {label.parent_concept for label in self.target_left_branch.labels}
                )
            )
        if self.target_right_branch is not None:
            right_branch_concepts = (
                StructureCollection({self.target_right_branch.parent_concept})
                if not isinstance(self.target_right_branch, Word)
                else StructureCollection(
                    {label.parent_concept for label in self.target_right_branch.labels}
                )
            )
        return (
            (self.target_root is None or self.target_root.parent_concept == rule.root)
            and (
                self.target_left_branch is None
                or rule.left_branch in left_branch_concepts
            )
            and (
                self.target_right_branch is None
                or rule.right_branch in right_branch_concepts
            )
        )
