from homer.location import Location
from homer.codelets.builders import ProjectionBuilder


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
            output_location,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        self.target_view.output_space.add(word)
        self.bubble_chamber.words.add(word)
        for location in word.locations:
            self.bubble_chamber.logger.log(location.space)
        self.bubble_chamber.logger.log(word)
        frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.target_projectee,
            end=word,
            locations=[self.target_projectee.location, word.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.target_view,
            quality=0.0,
        )
        self.child_structures = self.bubble_chamber.new_structure_collection(
            word, frame_to_output_correspondence
        )
        if self.target_projectee.is_slot:
            non_frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=self.non_frame_correspondee,
                end=word,
                locations=[
                    self.non_frame_correspondee.location_in_space(self.non_frame),
                    word.location,
                ],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.target_correspondence.conceptual_space,
                parent_view=self.target_view,
                quality=0.0,
            )
            self.child_structures.add(non_frame_to_output_correspondence)
