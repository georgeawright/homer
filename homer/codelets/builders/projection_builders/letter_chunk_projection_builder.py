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
            output_location = Location(
                self.target_projectee.location.coordinates,
                self.target_view.output_space,
            )
            word = self.target_projectee.abstract_chunk.copy_to_location(
                output_location,
                parent_id=self.codelet_id,
                bubble_chamber=self.bubble_chamber,
            )
        else:
            abstract_chunk = self._get_abstract_chunk()
            output_location = Location(
                self.target_projectee.location.coordinates,
                self.target_view.output_space,
            )
            locations = [
                location
                for location in abstract_chunk.locations
                if location.space.is_conceptual_space
            ] + [output_location]
            word = self.bubble_chamber.new_letter_chunk(
                name=abstract_chunk.name,
                locations=locations,
                parent_space=self.target_view.output_space,
                abstract_chunk=abstract_chunk,
            )
            for member in abstract_chunk.left_branch:
                if member.has_correspondence_to_space(self.target_view.output_space):
                    correspondence = member.correspondences_to_space(
                        self.target_view.output_space
                    ).get()
                    correspondee = correspondence.end
                    word.left_branch.add(correspondee)
                    word.members.add(correspondee)
                    correspondee.super_chunks.add(word)
            for member in abstract_chunk.right_branch:
                if member.has_correspondence_to_space(self.target_view.output_space):
                    correspondence = member.correspondences_to_space(
                        self.target_view.output_space
                    ).get()
                    correspondee = correspondence.end
                    word.right_branch.add(correspondee)
                    word.members.add(correspondee)
                    correspondee.super_chunks.add(word)
            for super_chunk in abstract_chunk.super_chunks:
                if super_chunk.has_correspondence_to_space(self.target_view.output):
                    correspondence = super_chunk.correspondences_to_space(
                        self.target_view.output_space
                    ).get()
                    correspondee = correspondence.end
                    if abstract_chunk in super_chunk.left_branch:
                        correspondee.left_branch.add(correspondee)
                    else:
                        correspondee.right_branch.add(correspondee)
                    correspondee.members.add(word)
                    word.super_chunks.add(correspondee)
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

    def _get_abstract_chunk(self):
        if not self.target_projectee.members.is_empty():
            return self.target_projectee
        if not self.target_projectee.correspondences.is_empty():
            return self.target_projectee.correspondees.get().abstract_chunk
        if not self.target_projectee.relations.is_empty():
            relation = self.target_projectee.relations.get()
            relative = self.target_projectee.relatives.get()
            relative_correspondee = (
                relative.correspondences_to_space(self.target_view.output_space)
                .get()
                .end
            )
            abstract_relation = relative_correspondee.abstract_chunk.relations.where(
                parent_concept=relation.parent_concept,
                start=relative_correspondee.abstract_chunk,
            ).get()
            return abstract_relation.arguments.get(
                exclude=[relative_correspondee.abstract_chunk]
            )
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
        return (
            meaning_concept.relations.where(parent_concept=grammar_concept)
            .get(key=lambda x: x.end.activation)
            .end
        )
