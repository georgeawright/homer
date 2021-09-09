from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.structures.spaces import Frame


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
        self.target_word = None
        self.target_correspondence = None
        self.word_correspondee = None
        self.non_frame_item = None

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
        # TODO
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def _structure_concept(self):
        raise NotImplementedError

    @property
    def target_structures(self):
        raise NotImplementedError
        return StructureCollection({self.target_view, self.target_word})

    def _passes_preliminary_checks(self):
        # check doesn't already exist
        raise NotImplementedError

    def _process_structure(self):
        # build item in output space
        # build correspondences from input spaces to new item
        raise NotImplementedError

    def _fizzle(self):
        pass
