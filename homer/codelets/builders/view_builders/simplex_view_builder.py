from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.views import SimplexView


class SimplexViewBuilder(ViewBuilder):
    @classmethod
    def get_target_class(cls):
        return SimplexView

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        target_one = bubble_chamber.spaces["input"]
        target_two = bubble_chamber.frames.get_active()
        urgency = urgency if urgency is not None else target_two.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target_one, target_two}),
            urgency,
        )
