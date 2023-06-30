import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structure_collection_keys import relating_salience
from linguoplotter.structures.links import Relation
from linguoplotter.structures.nodes import Concept
from linguoplotter.structures.spaces import ConceptualSpace


class RelationSuggester(Suggester):
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
        ).get(key=relating_salience)
        urgency = urgency if urgency is not None else start.unrelatedness
        targets = bubble_chamber.new_dict({"start": start}, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        conceptual_space: ConceptualSpace = None,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        if conceptual_space is None:
            conceptual_space = input_space.conceptual_spaces.filter(
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
                    start=x[0], end=x[1], space=conceptual_space
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
                "space": conceptual_space,
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
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=self.targets["space"],
                start=self.targets["start"],
                end=self.targets["end"],
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
                space.no_of_dimensions == 1
                and concept
                in (
                    self.bubble_chamber.concepts["same"],
                    self.bubble_chamber.concepts["more"],
                    self.bubble_chamber.concepts["less"],
                )
            )
            or (
                space.no_of_dimensions != 1
                and concept.parent_space == self.bubble_chamber.spaces["same-different"]
            )
        ]
        try:
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"],
                    end=x["end"],
                    concept=x["concept"],
                    space=x["space"],
                )
                / x["concept"].number_of_components,
            )
        except MissingStructureError:
            return False
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
        start_time = end.location_in_space(
            self.bubble_chamber.spaces["time"]
        ).coordinates[0][0]
        end_time = start.location_in_space(
            self.bubble_chamber.spaces["time"]
        ).coordinates[0][0]
        time_diff = abs(start_time - end_time)
        times_are_adjacent = 1 if time_diff <= 24 else 0.0
        sameness_relations = self.targets["start"].relations.filter(
            lambda x: x.parent_concept == self.bubble_chamber.concepts["same"]
            and self.targets["end"] in x.arguments
        )
        pair_sameness = (
            0
            if sameness_relations.is_empty
            else max([relation.quality for relation in sameness_relations])
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
            / (
                1
                if not self.targets["concept"].is_compound_concept
                else self.targets["concept"].number_of_components - 1
            )
            * times_are_adjacent
            * (
                pair_sameness
                if self.targets["concept"] != self.bubble_chamber.concepts["same"]
                else 1
            )
        )

    def _fizzle(self):
        if None in [
            self.targets["concept"],
            self.targets["space"],
            self.targets["end"],
        ]:
            return
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
            if start.relations.filter(
                lambda x: x.end == end
                and x.parent_concept == concept
                and x.conceptual_space == space
                and x.activation > 0
            ).is_empty
            and (start == self.targets["start"] or concept == self.targets["concept"])
            # top down relation suggesters are spawned either:
            # because an active concept is being searched for hence the concept should be kept the same
            # or because a frame's slot needs to be filled hence the arguments shoudld be kept the same
        ]
        try:
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"],
                    end=x["end"],
                    concept=x["concept"],
                    space=x["space"],
                ),
            )
            try:
                targets["start_view"] = self.targets["start_view"]
                targets["end_view"] = self.targets["end_view"]
            except KeyError:
                pass
            self.child_codelets.append(
                type(self).spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    targets["concept"].classifier.classify(
                        start=targets["start"],
                        end=targets["end"],
                        concept=targets["concept"],
                        space=targets["space"],
                    ),
                )
            )
        except MissingStructureError:
            pass
