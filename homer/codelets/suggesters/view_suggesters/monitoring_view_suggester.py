from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection


class MonitoringViewSuggester(ViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import MonitoringViewBuilder

        return MonitoringViewBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        text_space = StructureCollection(
            {
                space
                for space in bubble_chamber.working_spaces
                if space.parent_concept == bubble_chamber.concepts["text"]
                and not space.contents.is_empty()
            }
        ).get_exigent()
        input_space = bubble_chamber.spaces["input"]
        urgency = urgency if urgency is not None else text_space.exigency
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({text_space, input_space}),
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-monitoring"]

    def _passes_preliminary_checks(self):
        for view in self.bubble_chamber.views:
            if (
                StructureCollection.intersection(view.input_spaces, self.target_spaces)
                == self.target_spaces
            ):
                return False
        if self.frame is None:
            for space in self.target_spaces:
                if space.is_frame:
                    self.frame = space
        return True
