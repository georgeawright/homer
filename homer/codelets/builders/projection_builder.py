from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection


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
        self._target_structures = target_structures
        self.target_view = None
        self.non_frame = None
        self.target_projectee = None
        self.target_correspondence = None
        self.frame_correspondee = None
        self.non_frame_correspondee = None

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
        return StructureCollection({self.target_view, self.target_projectee})

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_correspondence = self._target_structures["target_correspondence"]
        self.target_projectee = self._target_structures["target_projectee"]
        self.frame_correspondee = self._target_structures["frame_correspondee"]
        self.non_frame = self._target_structures["non_frame"]
        self.non_frame_correspondee = self._target_structures["non_frame_correspondee"]
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
