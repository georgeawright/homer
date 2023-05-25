from linguoplotter.codelets.builders import LabelBuilder


class CrossViewLabelBuilder(LabelBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.label_evaluators import (
            CrossViewLabelEvaluator,
        )

        return CrossViewLabelEvaluator

    def _passes_preliminary_checks(self):
        equivalent_labels = self.targets["start"].labels.filter(
            lambda x: x.is_cross_view
            and x.parent_concept == self.targets["concept"]
            and x.has_location_in_space(self.targets["space"])
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
            is_cross_view=True,
        )
        self._structure_concept.instances.add(label)
        self._structure_concept.recalculate_salience()
        self.child_structures.add(label)
