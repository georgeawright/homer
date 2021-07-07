from homer.bubble_chamber import BubbleChamber
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.codelets.builders import PhraseBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence


class PhraseProjectionBuilder(PhraseBuilder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        PhraseBuilder.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )
        self.target_correspondence = None
        self.target_view = None

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

    def _passes_preliminary_checks(self) -> bool:
        self.target_correspondence = self._target_structures["target_correspondence"]
        self.target_view = self.target_correspondence.parent_view
        return not self.target_correspondence.start.has_correspondence_to_space(
            self.target_view.output_space
        )

    def _process_structure(self):
        new_phrase = self.target_correspondence.start.copy(
            bubble_chamber=self.bubble_chamber,
            parent_id=self.codelet_id,
            parent_space=self.target_view.output_space,
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
        pass
