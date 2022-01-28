from homer.location import Location
from homer.codelets.builders import ProjectionBuilder


class LetterChunkProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.projection_evaluators import (
            LetterChunkProjectionEvaluator,
        )

        return LetterChunkProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["letter-chunk"]

    def _process_structure(self):
        if not self.target_projectee.is_slot:
            abstract_chunk = self.target_projectee.abstract_chunk
        elif not self.target_projectee.correspondences.is_empty():
            abstract_chunk = self.target_projectee.correspondees.get().abstract_chunk
        elif not self.target_projectee.relations.is_empty():
            relation = self.target_projectee.relations.get()
            relative = self.target_projectee.relatives.get()
            abstract_relation = relative.abstract_chunk.relations.where(
                parent_concept=relation.parent_concept
            ).get()
            abstract_chunk = abstract_relation.arguments.get(
                exclude=[relative.abstract_chunk]
            )
        else:
            grammar_label = self.target_projectee.labels.filter(
                lambda x: x.parent_concept.parent_space
                == self.bubble_chamber.conceptual_spaces["grammar"]
            ).get()
            grammar_concept = (
                grammar_label.parent_concept
                if not grammar_label.parent_concept.is_slot
                else grammar_label.parent_concept.relatives.where(is_slot=False).get()
            )
            meaning_label = self.target_projectee.labels.filter(
                lambda x: x.parent_concept.parent_space
                != self.bubble_chamber.conceptual_spaces["grammar"]
            ).get()
            meaning_concept = (
                meaning_label.parent_concept
                if not meaning_label.parent_concept.is_slot
                else meaning_label.parent_concept.relatives.where(is_slot=False).get()
            )
            abstract_chunk = (
                meaning_concept.relations.where(parent_concept=grammar_concept)
                .get(key=lambda x: x.end.activation)
                .end
            )
        output_location = Location(
            self.target_projectee.location.coordinates,
            self.target_view.output_space,
        )
        word = abstract_chunk.copy_to_location(
            output_location,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
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
