from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import RelationSuggester
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import relating_exigency
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures.links import Relation
from linguoplotter.structures.nodes import Concept


class InterspatialRelationSuggester(RelationSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.relation_builders import (
            InterspatialRelationBuilder,
        )

        return InterspatialRelationBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        view = bubble_chamber.views.filter(
            lambda x: x.unhappiness < cls.FLOATING_POINT_TOLERANCE
            and x.parent_frame.parent_concept.location_in_space(
                bubble_chamber.spaces["grammar"]
            )
            == bubble_chamber.concepts["sentence"].location_in_space(
                bubble_chamber.spaces["grammar"]
            )
        ).get()
        start = view.output_space.contents.filter(
            lambda x: x.is_letter_chunk
            and x.members.is_empty
            and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
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
        view = bubble_chamber.views.filter(
            lambda x: x.unhappiness < cls.FLOATING_POINT_TOLERANCE
            and x.parent_frame.parent_concept.location_in_space(
                bubble_chamber.spaces["grammar"]
            )
            == bubble_chamber.concepts["sentence"].location_in_space(
                bubble_chamber.spaces["grammar"]
            )
        ).get()
        potential_spaces = view.output_space.conceptual_spaces.filter(
            lambda x: not x.is_symbolic
            and (
                x.no_of_dimensions == 1
                if parent_concept.parent_space.name == "more-less"
                else True
            )
        )
        potential_targets = view.output_space.contents.filter(
            lambda x: x.is_letter_chunk
            and x.members.is_empty
            and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
        ).get(key=relating_exigency)
        potential_pairs = [
            (a, b) for a in potential_targets for b in potential_targets if a != b
        ]
        possible_target_combos = [
            bubble_chamber.new_dict(
                {
                    "start": pair[0],
                    "end": pair[1],
                    "space": space,
                    "concept": parent_concept,
                },
                name="targets",
            )
            for pair in potential_pairs
            for space in potential_spaces
            if pair[0].has_location_in_space(space)
            and pair[1].has_location_in_space(space)
        ]
        targets = bubble_chamber.random_machine.select(
            possible_target_combos,
            key=lambda x: x["concept"].classifier.classify(
                start=x["start"],
                end=x["end"],
                concept=x["concept"],
                space=x["space"],
            ),
        )
        targets.name = "targets"
        urgency = urgency if urgency is not None else targets["start"].unrelatedness
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

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
            possible_ends = StructureSet.union(
                *[
                    view.output_space.contents.filter(
                        lambda x: x.is_letter_chunk
                        and x.members.is_empty
                        and x.parent_spaces.where(is_conceptual_space=True)
                        == self.targets["start"].parent_spaces.where(
                            is_conceptual_space=True
                        )
                    )
                    for view in self.bubble_chamber.views.filter(
                        lambda x: x.output_space != self.targets["start"].parent_space
                    )
                ]
            )
        else:
            possible_ends = [self.targets["end"]]
        if self.targets["space"] is None:
            possible_spaces = self.targets["start"].parent_spaces.where(
                is_conceptual_space=True
            )
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
        self.confidence = classification / self.targets["concept"].number_of_components
