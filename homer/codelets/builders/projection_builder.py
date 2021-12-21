from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


class ProjectionBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_structures.get("target_view")
        self.non_frame = target_structures.get("non_frame")
        self.target_projectee = target_structures.get("target_projectee")
        self.target_correspondence = target_structures.get("target_correspondence")
        self.frame_correspondee = target_structures.get("frame_correspondee")
        self.non_frame_correspondee = target_structures.get("non_frame_correspondee")

    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def target_structures(self):
        return self.bubble_chamber.new_structure_collection(
            self.target_view, self.target_projectee
        )

    @property
    def targets_dict(self):
        return {
            "target_view": self.target_view,
            "non_frame": self.non_frame,
            "target_projectee": self.target_projectee,
            "target_correspondence": self.target_correspondence,
            "frame_correspondee": self.frame_correspondee,
            "non_frame_correspondee": self.non_frame_correspondee,
        }

    def _passes_preliminary_checks(self):
        if self.target_projectee.is_slot:
            return (
                self.frame_correspondee.structure_id in self.target_view.slot_values
                and self.target_projectee.structure_id
                not in self.target_view.slot_values
            )
        return not self.target_projectee.has_correspondence_to_space(
            self.target_view.output_space
        )

    def _process_structure(self):
        raise NotImplementedError

    def _fizzle(self):
        pass
