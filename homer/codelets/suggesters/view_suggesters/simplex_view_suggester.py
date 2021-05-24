from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import WorkingSpace
from homer.structures.views import SimplexView


class SimplexViewSuggester(ViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        target_one = bubble_chamber.spaces["input"]
        target_two = bubble_chamber.frames.where(
            parent_concept=bubble_chamber.concepts["text"]
        ).get_active()
        urgency = urgency if urgency is not None else target_two.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target_one, target_two}),
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]
