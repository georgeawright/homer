import statistics
from typing import List, Union

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Chunk, Concept, Phrase, Word


class PhraseBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_root: Phrase,
        target_left_branch: Union[Phrase, Word],
        target_right_branch: Union[Phrase, Word],
        urgency: FloatBetweenOneAndZero,
        target_rule: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_rule = target_rule
        self.target_root = target_root
        self.target_left_branch = target_left_branch
        self.target_right_branch = target_right_branch
        self.parent_space = self.target_structures[0].parent_space
        self.child_structure = None

    @classmethod
    def get_target_class(cls):
        return Phrase

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_root: Phrase,
        target_left_branch: Union[Phrase, Word],
        target_right_branch: Union[Phrase, Word],
        urgency: FloatBetweenOneAndZero,
        target_rule: Concept = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_root,
            target_left_branch,
            target_right_branch,
            urgency,
            target_rule=target_rule,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_one = bubble_chamber.text_fragments.get_unhappy()
        target_two = target_one.potential_rule_mates.get_unhappy()
        try:
            target_three = StructureCollection.intersection(
                target_one.potential_rule_mates, target_two.potential_rule_mates
            ).get_unhappy()
            targets = StructureCollection({target_one, target_two, target_three})
        except MissingStructureError:
            targets = StructureCollection({target_one, target_two})
        target_root = None
        for target in targets:
            remaining_targets = StructureCollection.difference(
                targets, StructureCollection({target})
            )
            if hasattr(target, "members") and target.members == remaining_targets:
                target_root = target
                target_left_branch = target_root.left_branch
                target_right_branch = target_root.right_branch
        if target_root is None:
            branch_one = targets.get_random()
            branch_two = targets.get_random(exclude=[branch_one])
            if (
                branch_one.location.coordinates[0][0]
                < branch_two.location.coordinates[0][0]
            ):
                target_left_branch = branch_one
                target_right_branch = branch_two
            else:
                target_left_branch = branch_two
                target_right_branch = branch_one
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([target.unhappiness for target in targets])
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_root,
            target_left_branch,
            target_right_branch,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["phrase"]

    @property
    def target_structures(self) -> List[Structure]:
        targets = [
            self.target_root,
            self.target_left_branch,
            self.target_right_branch,
        ]
        return [target for target in targets if target is not None]

    def _passes_preliminary_checks(self):
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

    def _process_structure(self):
        if len(self.target_structures) == 2:
            chunk = Chunk(
                structure_id=ID.new(Chunk),
                parent_id=self.codelet_id,
                value=None,
                locations=[Location([], self.parent_space)],
                members=StructureCollection(),
                parent_space=self.parent_space,
                quality=1.0,
            )
            label = Label(
                structure_id=ID.new(Label),
                parent_id=self.codelet_id,
                start=chunk,
                parent_concept=self.target_rule.root,
                parent_space=self.parent_space,
                quality=1.0,
            )
            phrase = Phrase(
                structure_id=ID.new(Phrase),
                parent_id=self.codelet_id,
                chunk=chunk,
                label=label,
                quality=0.0,
                rule=self.target_rule,
            )
            phrase.activation = self.INITIAL_STRUCTURE_ACTIVATION
            self.parent_space.add(phrase)
            self.bubble_chamber.phrases.add(phrase)
            self.bubble_chamber.logger.log(chunk)
            self.bubble_chamber.logger.log(label)
            self.bubble_chamber.logger.log(phrase)
            self.child_structure = phrase
            if self.target_root is None:
                self.target_root = phrase
            elif self.target_left_branch is None:
                self.target_left_branch = phrase
            elif self.target_right_branch is None:
                self.target_right_branch = phrase
        slot_target = [target for target in self.target_structures if target.is_slot][0]
        if slot_target in [self.target_left_branch, self.target_right_branch]:
            self.target_root.chunk.members.add(slot_target)
        if slot_target == self.target_root:
            self.target_root.chunk.members.add(self.target_left_branch)
            self.target_root.chunk.members.add(self.target_right_branch)
            phrase.left_branch = self.target_left_branch
            phrase.right_branch = self.target_right_branch
            self.target_root.chunk.value = (
                f"{self.target_left_branch.value} {self.target_right_branch.value}"
            )
            self.target_root.chunk.locations = [
                Location.merge(
                    self.target_left_branch.location, self.target_right_branch.location
                )
            ]
            self.child_structure = self.target_root
        self.bubble_chamber.logger.log(self.target_root.chunk)
        self.bubble_chamber.logger.log(self.target_root)

    def _fizzle(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )

    def _fail(self):
        pass

    def _rule_is_compatible_with_targets(self, rule: Concept):
        left_branch_concepts = (
            StructureCollection({self.target_left_branch.parent_concept})
            if isinstance(self.target_left_branch, Phrase)
            else StructureCollection(
                {label.parent_concept for label in self.target_left_branch.labels}
            )
        )
        right_branch_concepts = (
            StructureCollection({self.target_right_branch.parent_concept})
            if isinstance(self.target_right_branch, Phrase)
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
