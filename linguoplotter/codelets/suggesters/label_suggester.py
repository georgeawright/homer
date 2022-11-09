from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import activation, labeling_exigency
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Concept


class LabelSuggester(Suggester):
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
            key=labeling_exigency
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
            if classification < 0.5:
                self.targets["concept"] = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.targets["concept"]]
                )
        else:
            try:
                conceptual_space = self.bubble_chamber.conceptual_spaces.filter(
                    lambda x: x.is_basic_level
                    and isinstance(self.targets["start"], x.instance_type)
                    and self.targets["start"].has_location_in_space(x)
                ).get()
                self.targets["start"].location_in_space(conceptual_space)
            except MissingStructureError:
                return False
            try:
                self.targets["concept"] = conceptual_space.contents.where(
                    is_concept=True, structure_type=Label, is_slot=False
                ).get(
                    key=lambda x: x.distance_function(
                        x.location_in_space(conceptual_space).coordinates,
                        self.targets["start"]
                        .location_in_space(conceptual_space)
                        .coordinates,
                    )
                )
            except MissingStructureError:
                try:
                    self.targets["concept"] = (
                        conceptual_space.contents.where(
                            is_concept=True, structure_type=Label
                        )
                        .where_not(classifier=None)
                        .get(
                            key=lambda x: x.distance_function(
                                x.location_in_space(conceptual_space).coordinates,
                                self.targets["start"]
                                .location_in_space(conceptual_space)
                                .coordinates,
                            )
                        )
                    )
                except MissingStructureError:
                    return False
        if self.targets["concept"] is None:
            return False
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
        pass
