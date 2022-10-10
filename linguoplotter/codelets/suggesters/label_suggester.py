from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.structure_collection_keys import activation, labeling_exigency
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Concept


class LabelSuggester(Suggester):
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
        self.target_node = target_structures.get("target_node")
        self.parent_concept = target_structures.get("parent_concept")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import LabelBuilder

        return LabelBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["parent_concept"] is not None else "BottomUp"
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
        space = bubble_chamber.input_spaces.get(key=activation)
        target = space.contents.filter(lambda x: x.is_chunk and x.quality > 0).get(
            key=labeling_exigency
        )
        urgency = urgency if urgency is not None else target.unlabeledness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_node": target, "parent_concept": None},
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        potential_targets = bubble_chamber.input_nodes.where(is_slot=False).filter(
            lambda x: isinstance(x, parent_concept.instance_type) and x.quality > 0
        )
        target = potential_targets.get(key=lambda x: parent_concept.proximity_to(x))
        urgency = urgency if urgency is not None else target.unlabeledness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_node": target, "parent_concept": parent_concept},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    @property
    def targets_dict(self):
        return {
            "target_node": self.target_node,
            "parent_concept": self.parent_concept,
        }

    def _passes_preliminary_checks(self):
        if self.parent_concept is not None:
            classification = self.parent_concept.classifier.classify(
                concept=self.parent_concept, start=self.target_node
            )
            if classification < 0.5:
                self.parent_concept = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.parent_concept]
                )
        else:
            try:
                conceptual_space = self.bubble_chamber.conceptual_spaces.filter(
                    lambda x: x.is_basic_level
                    and isinstance(self.target_node, x.instance_type)
                    and self.target_node.has_location_in_space(x)
                ).get()
                location = self.target_node.location_in_space(conceptual_space)
            except MissingStructureError:
                return False
            try:
                self.parent_concept = conceptual_space.contents.where(
                    is_concept=True, structure_type=Label, is_slot=False
                ).get(
                    key=lambda x: x.distance_function(
                        x.location_in_space(conceptual_space).coordinates,
                        self.target_node.location_in_space(
                            conceptual_space
                        ).coordinates,
                    )
                )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found parent concept: {self.parent_concept}"
                )
            except MissingStructureError:
                try:
                    self.parent_concept = (
                        conceptual_space.contents.where(
                            is_concept=True, structure_type=Label
                        )
                        .where_not(classifier=None)
                        .get(
                            key=lambda x: x.distance_function(
                                x.location_in_space(conceptual_space).coordinates,
                                self.target_node.location_in_space(
                                    conceptual_space
                                ).coordinates,
                            )
                        )
                    )
                    self.bubble_chamber.loggers["activity"].log(
                        self, f"Found parent concept: {self.parent_concept}"
                    )
                except MissingStructureError:
                    return False
        if self.parent_concept is None:
            return False
        return True

    def _calculate_confidence(self):
        classification = self.parent_concept.classifier.classify(
            concept=self.parent_concept, start=self.target_node
        )
        self.confidence = (
            classification
            * self.target_node.quality
            / self.parent_concept.number_of_components
        )

    def _fizzle(self):
        pass
