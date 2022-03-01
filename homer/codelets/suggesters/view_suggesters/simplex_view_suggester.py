from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.errors import MissingStructureError
from homer.structure_collection_keys import activation


class SimplexViewSuggester(ViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        contextual_space = bubble_chamber.input_spaces.get(key=activation)
        frame = bubble_chamber.frames.where(is_sub_frame=False).get(key=activation)
        views_with_frame = bubble_chamber.views.filter(
            lambda x: x.parent_frame in frame.instances or x.parent_frame == frame
        )
        print(len(views_with_frame))
        urgency = (
            urgency
            if urgency is not None
            else frame.activation
            * 0.5 ** sum([1 - view.activation for view in views_with_frame])
        )
        print(urgency)
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

    def _passes_preliminary_checks(self) -> bool:
        self.bubble_chamber.loggers["activity"].log(
            self, f"frame activation: {self.frame.activation}"
        )
        input_space_concept = self.contextual_space.parent_concept
        frame_input_space = (
            self.frame.input_space
            if self.frame.input_space.parent_concept == input_space_concept
            else self.frame.output_space
        )
        for conceptual_space in frame_input_space.conceptual_spaces:
            if (
                not conceptual_space.is_slot
                and conceptual_space not in self.contextual_space.conceptual_spaces
            ):
                self.bubble_chamber.loggers["activity"].log(
                    self,
                    f"{conceptual_space} is not a slot and "
                    + f"is not in {self.contextual_space} conceptual spaces",
                )
                return False
            if conceptual_space.is_slot:
                try:
                    self.conceptual_spaces_map[
                        conceptual_space
                    ] = self.contextual_space.conceptual_spaces.filter(
                        lambda x: x not in self.conceptual_spaces_map.values()
                        and conceptual_space.subsumes(x)
                    ).get(
                        key=activation
                    )
                except MissingStructureError:
                    self.bubble_chamber.loggers["activity"].log_dict(
                        self, self.conceptual_spaces_map, "Conceptual Space Map"
                    )
                    self.bubble_chamber.loggers["activity"].log(
                        self,
                        f"Unable to find space subsumed by {conceptual_space.structure_id}",
                    )
                    return False
        return True
