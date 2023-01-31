from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.codelets.suggesters import LabelSuggester
from linguoplotter.structure_collection_keys import labeling_exigency
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures.links import Label, Relation
from linguoplotter.structures.nodes import Concept


class InterspatialLabelSuggester(LabelSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.label_builders import (
            InterspatialLabelBuilder,
        )

        return InterspatialLabelBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        view = bubble_chamber.views.filter(
            lambda x: x.unhappiness < cls.FLOATING_POINT_TOLERANCE
            and x.parent_frame.parent_concept == bubble_chamber.concepts["sentence"]
        ).get(
            key=lambda x: fuzzy.OR(
                x in bubble_chamber.worldview.views,
                x.super_views.not_empty,
                x.activation,
            )
        )
        start = view.output_space.contents.filter(
            lambda x: x.is_letter_chunk
            and x.members.is_empty
            and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
        ).get(key=labeling_exigency)
        urgency = urgency if urgency is not None else start.unlabeledness
        targets = bubble_chamber.new_dict({"start": start}, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    def _passes_preliminary_checks(self):
        if not None in [self.targets["concept"], self.targets["space"]]:
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=self.targets["space"],
                start=self.targets["start"],
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < self.bubble_chamber.random_machine.generate_number():
                return False
        else:
            if self.targets["concept"] is None:
                possible_concepts = StructureSet.union(
                    *[
                        space.contents.filter(
                            lambda x: x.is_concept
                            and x.structure_type == Label
                            and x.classifier is not None
                        )
                        for space in self.bubble_chamber.conceptual_spaces.filter(
                            lambda x: x.structure_type == Relation
                        )
                    ]
                )
            else:
                possible_concepts = [self.targets["concept"]]
            if self.targets["space"] is None:
                possible_spaces = self.targets["start"].parent_spaces.filter(
                    lambda x: x.is_conceptual_space
                    and x.no_of_dimensions == 1
                    and not x.is_symbolic
                )
            else:
                possible_spaces = [self.targets["space"]]
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {
                    "start": self.targets["start"],
                    "space": space,
                    "concept": concept,
                },
                name="targets",
            )
            for space in possible_spaces
            for concept in possible_concepts
        ]
        self.targets = self.bubble_chamber.random_machine.select(
            possible_target_combos,
            key=lambda x: x["concept"].classifier.classify(
                start=x["start"],
                concept=x["concept"],
                space=x["space"],
            ),
        )
        return True

    def _calculate_confidence(self):
        classification = self.targets["concept"].classifier.classify(
            concept=self.targets["concept"],
            space=self.targets["space"],
            start=self.targets["start"],
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = (
            classification
            * self.targets["start"].quality
            / self.targets["concept"].number_of_components
        )

    def _fizzle(self):
        pass
