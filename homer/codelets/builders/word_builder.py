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


# TODO: rename to WordProjectionBuilder?
class WordBuilder(Builder):
    """Builds a word in an output space
    and correspondences to the items it refers to in input spaces"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.frame = None
        self.non_frame = None
        self.target_word = target_word
        self.target_non_frame_item = None
        self.target_correspondence = None
        self.child_structure = None

    @classmethod
    def get_target_class(cls):
        return Word

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_word,
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
            else bubble_chamber.views.get_unhappy()
        )
        frame = target_view.input_spaces.of_type(Frame).get_random()
        target_word = frame.contents.of_type(Word).get_exigent()
        urgency = urgency if urgency is not None else target_word.exigency
        return cls.spawn(parent_id, bubble_chamber, target_view, target_word, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _passes_preliminary_checks(self):
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
            if self.target_correspondence is not None
            else 1.0
        )

    def _process_structure(self):
        if self.target_word.is_slot:
            word_concept = self.target_view.slot_values[
                self.word_correspondee.structure_id
            ]
            lexeme = word_concept.lexemes.get_random()
            word_form = self.target_word.word_form
            self.target_view.slot_values[self.target_word.structure_id] = lexeme.forms[
                word_form
            ]
        else:
            lexeme = self.target_word.lexeme
            word_form = self.target_word.word_form
        word_location = Location(
            self.target_word.location.coordinates,
            self.target_view.output_space,
        )
        word = Word(
            ID.new(Word),
            self.codelet_id,
            lexeme=lexeme,
            word_form=word_form,
            location=word_location,
            parent_space=self.target_view.output_space,
            quality=0.0,
        )
        self.child_structure = word
        self.bubble_chamber.words.add(word)
        self.bubble_chamber.logger.log(word)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_word,
            end=self.child_structure,
            start_space=self.target_word.parent_space,
            end_space=self.target_view.output_space,
            locations=[self.target_word.location, word.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.target_view.output_space.conceptual_space,
            parent_view=self.target_view,
            quality=0.0,
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_word.links_in.add(frame_to_output_correspondence)
        self.target_word.links_out.add(frame_to_output_correspondence)
        word.links_in.add(frame_to_output_correspondence)
        word.links_out.add(frame_to_output_correspondence)
        if self.target_word.is_slot:
            non_frame_to_output_correspondence = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                start=self.non_frame_item,
                end=self.child_structure,
                start_space=self.non_frame,
                end_space=self.target_view.output_space,
                locations=[
                    self.non_frame_item.location_in_space(self.non_frame),
                    word.location,
                ],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.target_view.output_space.conceptual_space,
                parent_view=self.target_view,
                quality=0.0,
            )
            self.bubble_chamber.correspondences.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            word.links_in.add(non_frame_to_output_correspondence)
            word.links_out.add(non_frame_to_output_correspondence)
            self.non_frame_item.links_in.add(non_frame_to_output_correspondence)
            self.non_frame_item.links_out.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)

    def _fizzle(self):
        self.child_codelets.append(
            self.make(
                self.codelet_id,
                self.bubble_chamber,
                target_view=self.target_view,
                urgency=self.urgency / 2,
            )
        )

    def _fail(self):
        from homer.codelets.selectors import CorrespondenceSelector

        self.child_codelets.append(
            CorrespondenceSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_correspondence,
                self.urgency,
            )
        )
