from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.structure_collection import StructureCollection


class ProjectionEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        # TODO
        structure_type = bubble_chamber.concepts["word"]
        word = bubble_chamber.input_nodes.where(is_word=True).get()
        correspondences = word.correspondences.where(end=word)
        target_structures = StructureCollection.union(
            StructureCollection({word}), correspondences
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_structures,
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        raise NotImplementedError
