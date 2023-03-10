from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class ProjectionBuilder(Builder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    def _passes_preliminary_checks(self):
        return not self.targets["projectee"].has_correspondence_to_space(
            self.targets["view"].output_space
        )

    def _process_structure(self):
        raise NotImplementedError

    def _fizzle(self):
        pass
