from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class CorrespondenceEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors import CorrespondenceSelector

        return CorrespondenceSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["correspondence"]
        view = bubble_chamber.production_views.get(key=activation)
        target = view.members.where(start_space=view.raw_input_space).get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target}),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["correspondence"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_correspondence = self.target_structures.get()
        self.confidence = target_correspondence.parent_concept.classifier.classify_link(
            space=target_correspondence.conceptual_space,
            concept=target_correspondence.parent_concept,
            start=target_correspondence.start,
            end=target_correspondence.end,
            view=target_correspondence.parent_view,
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
