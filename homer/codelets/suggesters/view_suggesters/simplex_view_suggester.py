from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class SimplexViewSuggester(ViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        contextual_space = bubble_chamber.contextual_spaces.get(key=activation)
        frame = bubble_chamber.frames.get(key=activation)
        urgency = urgency if urgency is not None else frame.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"frame": frame, "contextual_space": contextual_space},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    @property
    def target_structures(self):
        return self.bubble_chamber.new_structure_collection(
            self.frame, self.contextual_space
        )
