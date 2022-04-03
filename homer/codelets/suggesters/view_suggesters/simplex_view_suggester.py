from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation
from homer.structures import Frame


class SimplexViewSuggester(ViewSuggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        ViewSuggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.frame = target_structures.get("frame")
        self.contextual_space = target_structures.get("contextual_space")
        self.prioritized_conceptual_spaces = target_structures.get(
            "prioritized_conceptual_spaces", bubble_chamber.new_structure_collection()
        )
        self.prioritized_targets = target_structures.get(
            "prioritized_targets", bubble_chamber.new_structure_collection()
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        frame: Frame = None,
        urgency: float = None,
    ):
        contextual_space = bubble_chamber.input_spaces.get(key=activation)
        if frame is None:
            frame = bubble_chamber.frames.where(is_sub_frame=False).get(key=activation)
        views_with_frame = bubble_chamber.views.filter(
            lambda x: x.parent_frame in frame.instances or x.parent_frame == frame
        )
        urgency = (
            urgency
            if urgency is not None
            else (1 - bubble_chamber.focus.focussedness)
            * frame.activation
            * 0.5 ** sum([1 - view.activation for view in views_with_frame])
        )
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
    def targets_dict(self):
        return {
            "frame": self.frame,
            "contextual_space": self.contextual_space,
            "conceptual_spaces_map": self.conceptual_spaces_map,
            "prioritized_targets": self.prioritized_targets,
            "prioritized_conceptual_spaces": self.prioritized_conceptual_spaces,
        }

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
                    ] = self.prioritized_conceptual_spaces.filter(
                        lambda x: x not in self.conceptual_spaces_map.values()
                        and conceptual_space.subsumes(x)
                    ).get(
                        key=activation
                    )
                except MissingStructureError:
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

    def _calculate_confidence(self):
        # if prioritized targets not empty, no view with same targets, 1
        # otherwise confidence divided by number of views with equivalent frame and space
        if not self.prioritized_targets.is_empty():
            equivalent_views = self.bubble_chamber.views.filter(
                lambda x: all(
                    [
                        x.input_spaces
                        == self.bubble_chamber.new_structure_collection(
                            self.contextual_space
                        ),
                        x.parent_frame.progenitor == self.frame.progenitor,
                        x.parent_frame.input_space.conceptual_spaces
                        == self.frame.input_space.conceptual_spaces,
                        x.prioritized_targets == self.prioritized_targets,
                        x.members.is_empty(),
                    ]
                )
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, equivalent_views, "Equivalent views"
            )
            self.confidence = 1 if equivalent_views.is_empty() else 0
        else:
            no_of_equivalent_views = len(
                self.bubble_chamber.views.filter(
                    lambda x: all(
                        [
                            x.input_spaces
                            == self.bubble_chamber.new_structure_collection(
                                self.contextual_space
                            ),
                            x.parent_frame.progenitor == self.frame.progenitor,
                        ]
                    )
                )
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Frame activation: {self.frame.activation}"
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Number of equivalent views: {no_of_equivalent_views}"
            )
            self.confidence = (
                self.frame.activation * 0.5 ** no_of_equivalent_views
                if no_of_equivalent_views > 0
                else self.frame.activation
            )
