from typing import Union

from homer.bubble_chamber import BubbleChamber
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.codelets.builders import PhraseBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence, Label
from homer.structures.nodes import Chunk, Phrase, Word
from homer.structures.spaces import WorkingSpace


class PhraseProjectionBuilder(PhraseBuilder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_correspondence: Correspondence,
        urgency: FloatBetweenOneAndZero,
    ):
        PhraseBuilder.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            None,
            None,
            None,
            urgency,
        )
        self.target_view = target_correspondence.parent_view
        self.target_correspondence = target_correspondence

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.phrase_evaluators import (
            PhraseProjectionEvaluator,
        )

        return PhraseProjectionEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_correspondence: Correspondence,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_correspondence,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.discourse_views.get_active()
        frame = target_view.input_frames.get_random()
        target_correspondence = StructureCollection(
            {
                member
                for member in target_view.members
                if member.start_space != frame
                and member.end_space != target_view.output_space
                and not member.start.has_correspondence_to_space(
                    target_view.output_space
                )
            }
        ).get_random()
        urgency = (
            urgency if urgency is not None else target_correspondence.start.unhappiness
        )
        return cls.spawn(parent_id, bubble_chamber, target_correspondence, urgency)

    def _passes_preliminary_checks(self) -> bool:
        return not self.target_correspondence.start.has_correspondence_to_space(
            self.target_view.output_space
        )

    def _calculate_confidence(self):
        self.confidence = self.target_correspondence.activation

    def _process_structure(self):
        new_phrase = self._copy_phrase_to_space(
            self.target_correspondence.start, self.target_view.output_space
        )
        input_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_correspondence.start,
            end=new_phrase,
            start_space=self.target_correspondence.start_space,
            end_space=self.target_view.output_space,
            locations=[
                self.target_correspondence.location_in_space(
                    self.target_correspondence.start_space
                ),
                new_phrase.location,
            ],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.target_view.output_space.conceptual_space,
            parent_view=self.target_view,
            quality=0.0,
        )
        self.bubble_chamber.correspondences.add(input_to_output_correspondence)
        self.bubble_chamber.logger.log(input_to_output_correspondence)
        self.target_correspondence.start.links_out.add(input_to_output_correspondence)
        self.target_correspondence.start.links_in.add(input_to_output_correspondence)
        new_phrase.links_out.add(input_to_output_correspondence)
        new_phrase.links_in.add(input_to_output_correspondence)
        self.target_view.members.add(input_to_output_correspondence)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_correspondence.end,
            end=new_phrase,
            start_space=self.target_correspondence.end_space,
            end_space=self.target_view.output_space,
            locations=[
                self.target_correspondence.location_in_space(
                    self.target_correspondence.end_space
                ),
                new_phrase.location,
            ],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.target_view.output_space.conceptual_space,
            parent_view=self.target_view,
            quality=0.0,
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_correspondence.end.links_out.add(input_to_output_correspondence)
        self.target_correspondence.end.links_in.add(input_to_output_correspondence)
        new_phrase.links_out.add(input_to_output_correspondence)
        new_phrase.links_in.add(input_to_output_correspondence)
        self.target_view.members.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)
        self.child_structures = StructureCollection(
            {new_phrase, input_to_output_correspondence, frame_to_output_correspondence}
        )

    def _fizzle(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )

    def _fail(self):
        self._fizzle()

    def _copy_phrase_to_space(
        self, phrase: Union[Phrase, Word], space: WorkingSpace
    ) -> Phrase:
        if phrase.is_word:
            return Word(
                ID.new(Word),
                self.codelet_id,
                lexeme=phrase.lexeme,
                word_form=phrase.word_form,
                location=Location(phrase.location.coordinates, space),
                parent_space=space,
                quality=phrase.quality,
            )
        new_left_branch = self._copy_phrase_to_space(phrase.left_branch, space)
        new_right_branch = self._copy_phrase_to_space(phrase.right_branch, space)
        new_chunk = Chunk(
            ID.new(Chunk),
            self.codelet_id,
            value=f"{new_left_branch.value} {new_right_branch.value}",
            locations=[
                Location.merge(new_left_branch.location, new_right_branch.location)
            ],
            members=StructureCollection({new_left_branch, new_right_branch}),
            parent_space=space,
            quality=1.0,
        )
        new_label = Label(
            ID.new(Label),
            self.codelet_id,
            start=new_chunk,
            parent_concept=phrase.rule.root,
            parent_space=space,
            quality=1.0,
        )
        return Phrase(
            ID.new(Phrase),
            self.codelet_id,
            chunk=new_chunk,
            label=new_label,
            quality=phrase.quality,
            left_branch=new_left_branch,
            right_branch=new_right_branch,
            rule=phrase.rule,
        )
