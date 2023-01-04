import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structure_collection_keys import relating_exigency
from linguoplotter.structures.links import Relation
from linguoplotter.structures.nodes import Concept


class RelationSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, targets, urgency
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import RelationBuilder

        return RelationBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = "TopDown" if targets["concept"] is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        start = input_space.contents.filter(
            lambda x: x.is_chunk and not x.is_slot and x.quality > 0
        ).get(key=relating_exigency)
        urgency = urgency if urgency is not None else start.unrelatedness
        targets = bubble_chamber.new_dict({"start": start}, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        target_space = input_space.conceptual_spaces.filter(
            lambda x: (
                x.no_of_dimensions == 1
                if parent_concept.parent_space.name == "more-less"
                else True
            )
            and (
                x in input_space.conceptual_spaces
                if parent_concept.parent_space.name == "same-different"
                else True
            )
        ).get()
        potential_targets = input_space.contents.filter(
            lambda x: x.is_node and x.is_slot and x.quality > 0
        )
        try:
            possible_pairs = [
                (a, b) for a in potential_targets for b in potential_targets if a != b
            ]
            start, end = bubble_chamber.random_machine.select(
                possible_pairs,
                key=lambda x: parent_concept.classifier.classify(
                    start=x[0], end=x[1], space=target_space
                ),
            )

        except NoLocationError:
            raise MissingStructureError
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([start.unrelatedness, end.unrelatedness])
        )
        targets = bubble_chamber.new_dict(
            {
                "start": start,
                "end": end,
                "space": target_space,
                "concept": parent_concept,
            },
            name="targets",
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if None not in [
            self.targets["concept"],
            self.targets["space"],
            self.targets["end"],
        ]:
            if any(
                [
                    self.targets["start"].is_slot
                    and not self.targets["start"].is_filled_in,
                    self.targets["end"].is_slot
                    and not self.targets["end"].is_filled_in,
                ]
            ):
                return False
            start = (
                self.targets["start"]
                if not self.targets["start"].is_slot
                else self.targets["start"].non_slot_value
            )
            end = (
                self.targets["end"]
                if not self.targets["end"].is_slot
                else self.targets["end"].non_slot_value
            )
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=self.targets["space"],
                start=start,
                end=end,
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < self.bubble_chamber.random_machine.generate_number():
                return False
            return True
        if self.targets["concept"] is None:
            possible_concepts = self.bubble_chamber.concepts.where(
                structure_type=Relation, is_slot=False
            ).where_not(classifier=None)
        else:
            possible_concepts = [self.targets["concept"]]
        if self.targets["end"] is None:
            possible_ends = self.targets["start"].parent_space.contents.filter(
                lambda x: x != self.targets["start"] and x.is_chunk and x.quality > 0
            )
        else:
            possible_ends = [self.targets["end"]]
        if self.targets["space"] is None:
            possible_spaces = self.targets[
                "start"
            ].parent_space.conceptual_spaces_and_sub_spaces
        else:
            possible_spaces = [self.targets["space"]]
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {
                    "start": self.targets["start"],
                    "end": end,
                    "space": space,
                    "concept": concept,
                },
                name="targets",
            )
            for end in possible_ends
            for space in possible_spaces
            for concept in possible_concepts
            if (
                space.no_of_dimensions == 1 and concept.parent_space.name == "more-less"
            )
            or (
                space in self.targets["start"].parent_space.conceptual_spaces
                and concept.parent_space.name == "same-different"
            )
        ]
        targets = self.bubble_chamber.random_machine.select(
            possible_target_combos,
            key=lambda x: x["concept"].classifier.classify(
                start=x["start"],
                end=x["end"],
                concept=x["concept"],
                space=x["space"],
            ),
        )
        self.targets["concept"], self.targets["end"], self.targets["space"] = (
            targets["concept"],
            targets["end"],
            targets["space"],
        )
        return True

    def _calculate_confidence(self):
        start = (
            self.targets["start"]
            if not self.targets["start"].is_slot
            else self.targets["start"].non_slot_value
        )
        end = (
            self.targets["end"]
            if not self.targets["end"].is_slot
            else self.targets["end"].non_slot_value
        )
        classification = self.targets["concept"].classifier.classify(
            concept=self.targets["concept"],
            space=self.targets["space"],
            start=start,
            end=end,
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = (
            classification
            * min(start.quality, end.quality)
            / self.targets["concept"].number_of_components
        )

    def _fizzle(self):
        if None in [
            self.targets["concept"],
            self.targets["space"],
            self.targets["end"],
        ]:
            return
        if any(
            [
                self.targets["start"].is_slot
                and not self.targets["start"].is_filled_in,
                self.targets["end"].is_slot and not self.targets["end"].is_filled_in,
            ]
        ):
            return False
        possible_target_pairs = [
            (self.targets["start"], self.targets["end"]),
            (self.targets["end"], self.targets["start"]),
        ]
        possible_spaces = [self.targets["space"]]
        original_concept = self.targets["concept"]
        negated_concept = self.bubble_chamber.new_compound_concept(
            self.bubble_chamber.concepts["not"], [self.targets["concept"]]
        )
        if negated_concept.reverse is None and original_concept.reverse is not None:
            negated_concept.reverse = self.bubble_chamber.new_compound_concept(
                self.bubble_chamber.concepts["not"], [original_concept.reverse]
            )
            negated_concept.reverse.reverse = negated_concept
        possible_concepts = [original_concept, negated_concept]
        if self.targets["concept"].is_compound_concept:
            for arg in self.targets["concept"].args:
                possible_concepts.append(arg)
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {"start": start, "end": end, "space": space, "concept": concept},
                name="targets",
            )
            for start, end in possible_target_pairs
            for space in possible_spaces
            for concept in possible_concepts
            if start.relations.where(
                end=end, parent_concept=concept, conceptual_space=space
            ).is_empty
        ]
        try:
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"]
                    if not x["start"].is_slot
                    else x["start"].non_slot_value,
                    end=x["end"] if not x["end"].is_slot else x["end"].non_slot_value,
                    concept=x["concept"],
                    space=x["space"],
                ),
            )
            self.child_codelets.append(
                RelationSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    targets["concept"].classifier.classify(
                        start=targets["start"]
                        if not targets["start"].is_slot
                        else targets["start"].non_slot_value,
                        end=targets["end"]
                        if not targets["end"].is_slot
                        else targets["end"].non_slot_value,
                        concept=targets["concept"],
                        space=targets["space"],
                    ),
                )
            )
        except MissingStructureError:
            pass
