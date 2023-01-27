from linguoplotter.codelets.builders import LabelBuilder


class InterspatialLabelBuilder(LabelBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.label_evaluators import (
            InterspatialLabelEvaluator,
        )

        return InterspatialLabelEvaluator

    def _process_structure(self):
        if self.child_structures.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Equivalent label already exists"
            )
            return
        conceptual_location = self.targets["start"].location_in_space(
            self.targets["space"]
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
            is_interspatial=True,
        )
        self._structure_concept.instances.add(label)
        self._structure_concept.recalculate_exigency()
        self.child_structures.add(label)
