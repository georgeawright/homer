from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import activation, labeling_salience
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Concept


class LabelSuggester(Suggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import LabelBuilder

        return LabelBuilder

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
        space = bubble_chamber.input_spaces.get(key=activation)
        start = space.contents.filter(lambda x: x.is_chunk and x.quality > 0).get(
            key=labeling_salience
        )
        urgency = urgency if urgency is not None else start.unlabeledness
        targets = bubble_chamber.new_dict({"start": start}, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        potential_starts = bubble_chamber.input_nodes.where(is_slot=False).filter(
            lambda x: isinstance(x, concept.instance_type) and x.quality > 0
        )
        start = potential_starts.get(key=lambda x: concept.proximity_to(x))
        urgency = (
            urgency
            if urgency is not None
            else start.unlabeledness * concept.proximity_to(start)
        )
        targets = bubble_chamber.new_dict(
            {"start": start, "concept": concept}, name="targets"
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.targets["concept"] is not None:
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"], start=self.targets["start"]
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < self.bubble_chamber.random_machine.generate_number():
                return False
        else:
            possible_concepts = StructureSet.union(
                *[
                    space.contents.where(
                        is_concept=True, structure_type=Label, is_slot=False
                    )
                    for space in self.targets["start"].parent_spaces.where(
                        is_conceptual_space=True
                    )
                ]
            )
            self.targets["concept"] = possible_concepts.get(
                key=lambda x: x.classifier.classify(
                    concept=x, start=self.targets["start"]
                )
                / x.number_of_components
            )
        return True

    def _calculate_confidence(self):
        classification = self.targets["concept"].classifier.classify(
            concept=self.targets["concept"], start=self.targets["start"]
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = (
            classification
            * self.targets["start"].quality
            / self.targets["concept"].number_of_components
        )

    def _fizzle(self):
        if self.targets["concept"] is None:
            return
        possible_concepts = [self.targets["concept"]]
        possible_concepts.append(
            self.bubble_chamber.new_compound_concept(
                self.bubble_chamber.concepts["not"], [self.targets["concept"]]
            )
        )
        if self.targets["concept"].is_compound_concept:
            for arg in self.targets["concept"].args:
                possible_concepts.append(arg)
        targets = self.bubble_chamber.new_dict(name="targets")
        targets["start"] = self.targets["start"]
        targets["concept"] = self.bubble_chamber.random_machine.select(
            possible_concepts,
            key=lambda x: x.classifier.classify(start=targets["start"], concept=x),
        )
        self.child_codelets.append(
            type(self).spawn(
                self.codelet_id,
                self.bubble_chamber,
                targets,
                targets["concept"].proximity_to(targets["start"]),
            )
        )
