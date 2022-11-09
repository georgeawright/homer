from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class LabelBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import LabelEvaluator

        return LabelEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        equivalent_labels = self.targets["start"].labels.where(
            parent_concept=self.targets["concept"]
        )
        if equivalent_labels.not_empty:
            self.child_structures.add(equivalent_labels.get())
        return True

    def _process_structure(self):
        if self.child_structures.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Equivalent label already exists"
            )
            return
        try:
            conceptual_location = self.targets["start"].location_in_space(
                self.targets["concept"].parent_basic_space
            )
        except (MissingStructureError, NoLocationError):
            try:
                conceptual_location = self.targets["start"].location_in_space(
                    self.targets["concept"].parent_space
                )
            except NoLocationError:
                conceptual_space = self.targets["concept"].parent_space
                self.targets["start"].parent_space.add_conceptual_space(
                    conceptual_space
                )
                conceptual_location = self.targets["start"].location_in_space(
                    conceptual_space
                )
        locations = [
            self.targets["start"].location_in_space(self.targets["start"].parent_space),
            conceptual_location,
        ]
        label = self.bubble_chamber.new_label(
            parent_id=self.codelet_id,
            start=self.targets["start"],
            parent_concept=self.targets["concept"],
            locations=locations,
            quality=0,
        )
        self._structure_concept.instances.add(label)
        self._structure_concept.recalculate_exigency()
        self.child_structures.add(label)

    def _fizzle(self):
        pass
