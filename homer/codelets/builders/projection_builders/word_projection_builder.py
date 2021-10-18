from homer.id import ID
from homer.location import Location
from homer.codelets.builders import ProjectionBuilder
from homer.structures.links import Correspondence


class WordProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.projection_evaluators import (
            WordProjectionEvaluator,
        )

        return WordProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _process_structure(self):
        if self.target_projectee.is_slot:
            word_concept = self.target_view.slot_values[
                self.frame_correspondee.structure_id
            ]
            lexeme = word_concept.lexemes.get()
            word_form = self.target_projectee.word_form
            abstract_word = self.bubble_chamber.words[lexeme.word_forms[word_form]]
            self.target_view.slot_values[
                self.target_projectee.structure_id
            ] = abstract_word.name
        else:
            abstract_word = self.target_projectee
        output_location = Location(
            self.target_projectee.location.coordinates,
            self.target_view.output_space,
        )
        word = abstract_word.copy_to_location(
            output_location, parent_id=self.codelet_id
        )
        self.target_view.output_space.add(word)
        self.bubble_chamber.words.add(word)
        for location in word.locations:
            self.bubble_chamber.logger.log(location.space)
        self.bubble_chamber.logger.log(word)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_projectee,
            arguments=self.bubble_chamber.new_structure_collection(
                self.target_projectee, word
            ),
            locations=[self.target_projectee.location, word.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.target_view,
            quality=0.0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        self.child_structures = self.bubble_chamber.new_structure_collection(
            word, frame_to_output_correspondence
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_view.members.add(frame_to_output_correspondence)
        self.target_projectee.links_in.add(frame_to_output_correspondence)
        self.target_projectee.links_out.add(frame_to_output_correspondence)
        word.links_in.add(frame_to_output_correspondence)
        word.links_out.add(frame_to_output_correspondence)
        for location in frame_to_output_correspondence.locations:
            location.space.add(frame_to_output_correspondence)
        if self.target_projectee.is_slot:
            non_frame_to_output_correspondence = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                start=self.non_frame_correspondee,
                arguments=self.bubble_chamber.new_structure_collection(
                    self.non_frame_correspondee, word
                ),
                locations=[
                    self.non_frame_correspondee.location_in_space(self.non_frame),
                    word.location,
                ],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.target_correspondence.conceptual_space,
                parent_view=self.target_view,
                quality=0.0,
                links_in=self.bubble_chamber.new_structure_collection(),
                links_out=self.bubble_chamber.new_structure_collection(),
                parent_spaces=self.bubble_chamber.new_structure_collection(),
            )
            self.child_structures.add(non_frame_to_output_correspondence)
            self.bubble_chamber.correspondences.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            self.target_view.members.add(non_frame_to_output_correspondence)
            word.links_in.add(non_frame_to_output_correspondence)
            word.links_out.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_in.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_out.add(
                non_frame_to_output_correspondence
            )
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            for location in non_frame_to_output_correspondence.locations:
                location.space.add(non_frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)
