from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk
from homer.structures.chunks import Word, Slot, View
from homer.structures.links import Correspondence
from homer.structures.spaces import Frame, WorkingSpace


class WordBuilder(Builder):
    """Builds a correspondence and a new item in an output space connected to it."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_frame_item: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.frame = None
        self.non_frame = None
        self.output_space = None
        self.target_frame_item = target_frame_item
        self.target_non_frame_item = None
        self.target_correspondence = None
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_frame_item: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_frame_item,
            urgency,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.views.get_unhappy()
        frame = target_view.input_spaces.of_type(Frame).get_random()
        target_frame_item = frame.contents.of_type(Chunk).get_exigent()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_view,
            target_frame_item,
            target_frame_item.exigency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _passes_preliminary_checks(self):
        self.frame = self.target_frame_item.parent_space
        self.non_frame = self.target_view.input_spaces.of_type(
            WorkingSpace
        ).get_random()
        self.output_space = self.target_view.output_space
        if isinstance(self.target_frame_item, Slot):
            try:
                self.target_correspondence = StructureCollection.union(
                    self.target_view.members.where(start=self.target_frame_item),
                    self.target_view.members.where(end=self.target_frame_item),
                ).get_active()
                self.target_non_frame_item = (
                    self.target_correspondence.get_non_slot_argument()
                )
            except MissingStructureError:
                return False
        return not self.target_frame_item.has_correspondence_to_space(self.output_space)

    def _calculate_confidence(self):
        self.confidence = (
            self.target_correspondence.activation
            if self.target_correspondence is not None
            else 1.0
        )

    def _process_structure(self):
        if self.target_correspondence is not None:
            compatible_labels = StructureCollection(
                {
                    label
                    for label in self.target_non_frame_item.labels
                    if label.parent_concept.parent_space.parent_concept
                    == self.target_frame_item.value
                }
            )
            concept = compatible_labels.get_active().parent_concept
            conceptual_space = concept.parent_space
            lexeme = concept.lexemes.get_active()
            word_value = lexeme.get_form(self.target_frame_item.form)
        else:
            conceptual_space = None
            lexeme = None
            word_value = self.target_frame_item.value
        word_location = Location(
            self.target_frame_item.location_in_space(self.frame).coordinates,
            self.output_space,
        )
        word = Word(
            ID.new(Word),
            self.codelet_id,
            word_value,
            lexeme,
            word_location,
            self.output_space,
            0,
        )
        self.bubble_chamber.logger.log(word)
        frame_to_output_space = self.bubble_chamber.get_super_space(
            self.frame, self.output_space
        )
        projection_from_frame = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            self.target_frame_item,
            word,
            Location.for_correspondence_between(
                self.target_frame_item.location_in_space(self.frame),
                word.location_in_space(self.output_space),
                frame_to_output_space,
            ),
            self.frame,
            self.output_space,
            self.bubble_chamber.concepts["same"],
            conceptual_space,
            0,
        )
        self.target_frame_item.links_out.add(projection_from_frame)
        word.links_in.add(projection_from_frame)
        frame_to_output_space.add(projection_from_frame)
        self.bubble_chamber.correspondences.add(projection_from_frame)
        self.target_view.members.add(projection_from_frame)
        self.bubble_chamber.logger.log(projection_from_frame)
        if self.target_correspondence is not None:
            non_frame_to_output_space = self.bubble_chamber.get_super_space(
                self.non_frame, self.output_space
            )
            projection_from_non_frame = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                self.target_non_frame_item,
                word,
                Location.for_correspondence_between(
                    self.target_non_frame_item.location_in_space(self.non_frame),
                    word.location_in_space(self.output_space),
                    non_frame_to_output_space,
                ),
                self.non_frame,
                self.output_space,
                self.bubble_chamber.concepts["same"],
                concept.parent_space,
                0,
            )
            self.bubble_chamber.logger.log(projection_from_non_frame)
            self.target_non_frame_item.links_out.add(projection_from_non_frame)
            word.links_in.add(projection_from_non_frame)
            non_frame_to_output_space.add(projection_from_non_frame)
            self.bubble_chamber.correspondences.add(projection_from_non_frame)
            self.target_view.members.add(projection_from_non_frame)
        self.output_space.add(word)
        self.bubble_chamber.words.add(word)
        self.child_structure = word
        self.bubble_chamber.logger.log(word)
        self.bubble_chamber.logger.log(self.target_view)

    def _engender_follow_up(self):
        from homer.codelets.evaluators import WordEvaluator

        self.child_codelets.append(
            WordEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        try:
            new_target_frame_item = self.frame.contents.of_type(Chunk).get_random(
                exclude=[self.target_frame_item]
            )
            self.child_codelets.append(
                self.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    self.target_view,
                    new_target_frame_item,
                    self.urgency / 2,
                )
            )
        except MissingStructureError:
            pass

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
