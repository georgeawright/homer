from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.structures.spaces import Frame


class WordSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = None
        self.non_frame = None
        self.target_word = None
        self.target_correspondence = None
        self.word_correspondee = None
        self.non_frame_item = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import WordBuilder

        return WordBuilder

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

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View = None,
        urgency: float = None,
    ):
        target_view = (
            target_view
            if target_view is not None
            else bubble_chamber.views.get_active()
        )
        frame = target_view.input_spaces.of_type(Frame).get_random()
        target_word = frame.contents.of_type(Word).get_exigent()
        urgency = urgency if urgency is not None else target_view.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_view": target_view, "target_word": target_word},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    @property
    def target_structures(self):
        return StructureCollection({self.target_view, self.target_word})

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_word = self._target_structures["target_word"]
        self._target_structures["word_correspondee"] = None
        self._target_structures["non_frame"] = None
        self._target_structures["non_frame_item"] = None
        try:
            self.word_correspondee = StructureCollection(
                {
                    correspondence.start
                    if correspondence.start != self.target_word
                    else correspondence.end
                    for correspondence in self.target_word.correspondences
                    if correspondence.start.is_slot and correspondence.end.is_slot
                }
            ).get_random()
            self._target_structures["word_correspondee"] = self.word_correspondee
            correspondence_to_non_frame_item = StructureCollection(
                {
                    correspondence
                    for correspondence in self.word_correspondee.correspondences
                    if (
                        not isinstance(correspondence.start_space, Frame)
                        or not isinstance(correspondence.end_space, Frame)
                    )
                    and correspondence in self.target_view.members
                }
            ).get_random()
            self.non_frame, self.non_frame_item = (
                (
                    correspondence_to_non_frame_item.start_space,
                    correspondence_to_non_frame_item.start,
                )
                if correspondence_to_non_frame_item.start != self.word_correspondee
                else (
                    correspondence_to_non_frame_item.end_space,
                    correspondence_to_non_frame_item.end,
                )
            )
            self._target_structures["non_frame"] = self.non_frame
            self._target_structures["non_frame_item"] = self.non_frame_item
            return (
                self.word_correspondee.structure_id in self.target_view.slot_values
                and self.target_word.structure_id not in self.target_view.slot_values
            )
        except MissingStructureError:
            return (
                not self.target_word.is_slot
                and not self.target_word.has_correspondence_to_space(
                    self.target_view.output_space
                )
            )

    def _calculate_confidence(self):
        self.confidence = (
            self.target_correspondence.activation
            # TODO: self.target_correspondence is always None
            if self.target_correspondence is not None
            else 1.0
        )

    def _fizzle(self):
        self.child_codelets.append(
            self.make(
                self.codelet_id,
                self.bubble_chamber,
                target_view=self.target_view,
                urgency=self.urgency / 2,
            )
        )
