from linguoplotter.location import Location
from linguoplotter.codelets.builders import ProjectionBuilder
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation


class LetterChunkProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.projection_evaluators import (
            LetterChunkProjectionEvaluator,
        )

        return LetterChunkProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["letter-chunk"]

    def _process_structure(self):
        if not self.targets["projectee"].is_slot:
            abstract_chunk = self.targets["projectee"].abstract_chunk
            output_location = Location(
                self.targets["projectee"].location.coordinates,
                self.targets["view"].output_space,
            )
            if abstract_chunk.members.is_empty:
                word = self.targets["projectee"].abstract_chunk.copy_to_location(
                    output_location,
                    parent_id=self.codelet_id,
                    bubble_chamber=self.bubble_chamber,
                )
            else:
                locations = [
                    location
                    for location in abstract_chunk.locations
                    if location.space.is_conceptual_space
                ] + [output_location]
                word = self.bubble_chamber.new_letter_chunk(
                    name=None,
                    locations=locations,
                    parent_space=self.targets["view"].output_space,
                    abstract_chunk=abstract_chunk,
                    parent_id=self.codelet_id,
                )
        else:
            abstract_chunk = self._get_abstract_chunk()
            self.bubble_chamber.loggers["activity"].log(
                f"Found abstract chunk: {abstract_chunk}"
            )
            self.targets["projectee"].abstract_chunk = abstract_chunk
            sameness_relations = self.targets["projectee"].links_in.where(
                is_relation=True, parent_concept=self.bubble_chamber.concepts["same"]
            )
            output_chunk_name = abstract_chunk.name
            if sameness_relations.not_empty:
                sameness_start_correspondences_to_output = (
                    sameness_relations.get().start.correspondences_to_space(
                        self.targets["view"].output_space
                    )
                )
                if sameness_start_correspondences_to_output.not_empty:
                    if (
                        sameness_start_correspondences_to_output.get().end.name
                        == abstract_chunk.name
                    ):
                        output_chunk_name = ""
            output_location = Location(
                self.targets["projectee"].location.coordinates,
                self.targets["view"].output_space,
            )
            locations = [
                location
                for location in abstract_chunk.locations
                if location.space.is_conceptual_space
            ] + [output_location]
            word = self.bubble_chamber.new_letter_chunk(
                name=output_chunk_name,
                locations=locations,
                parent_space=self.targets["view"].output_space,
                abstract_chunk=abstract_chunk,
                parent_id=self.codelet_id,
            )
            self.bubble_chamber.loggers["activity"].log(f"Built Letter Chunk {word}")
            self.bubble_chamber.loggers["activity"].log(
                f"Left branch {word.left_branch}"
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Right branch {word.right_branch}"
            )
        for member in self.targets["projectee"].left_branch:
            if member.has_correspondence_to_space(self.targets["view"].output_space):
                correspondence = member.correspondences_to_space(
                    self.targets["view"].output_space
                ).get()
                correspondee = correspondence.end
                self.bubble_chamber.loggers["activity"].log(
                    f"Adding {correspondee} to left branch of {word}"
                )
                word.left_branch.add(correspondee)
                word.members.add(correspondee)
                word.sub_chunks.add(correspondee)
                correspondee.super_chunks.add(word)
        for member in self.targets["projectee"].right_branch:
            if member.has_correspondence_to_space(self.targets["view"].output_space):
                correspondence = member.correspondences_to_space(
                    self.targets["view"].output_space
                ).get()
                correspondee = correspondence.end
                self.bubble_chamber.loggers["activity"].log(
                    f"Adding {correspondee} to right branch of {word}"
                )
                word.right_branch.add(correspondee)
                word.members.add(correspondee)
                word.sub_chunks.add(correspondee)
                correspondee.super_chunks.add(word)
        for super_chunk in self.targets["projectee"].super_chunks:
            if super_chunk.has_correspondence_to_space(
                self.targets["view"].output_space
            ):
                correspondence = super_chunk.correspondences_to_space(
                    self.targets["view"].output_space
                ).get()
                correspondee = correspondence.end
                if self.targets["projectee"] in super_chunk.left_branch:
                    self.bubble_chamber.loggers["activity"].log(
                        f"Adding {word} to left branch of {correspondee}"
                    )
                    correspondee.left_branch.add(word)
                elif self.targets["projectee"] in super_chunk.right_branch:
                    self.bubble_chamber.loggers["activity"].log(
                        f"Adding {word} to right branch of {correspondee}"
                    )
                    correspondee.right_branch.add(word)
                correspondee.members.add(word)
                correspondee.sub_chunks.add(word)
                word.super_chunks.add(correspondee)
        frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.targets["projectee"],
            end=word,
            locations=[self.targets["projectee"].location, word.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.targets["view"],
            quality=0.0,
        )
        self.child_structures.add(word)
        self.child_structures.add(frame_to_output_correspondence)
        self.bubble_chamber.loggers["structure"].log_view(self.targets["view"])

    def _get_abstract_chunk(self):
        if self.targets["projectee"].members.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Target projectee is abstract chunk"
            )
            return self.targets["projectee"]
        if self.targets["projectee"].correspondences.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Correspondee to target projectee is abstract chunk"
            )
            return self._get_abstract_chunk_from_correspondence()
        if self.targets["projectee"].links_in.where(is_relation=True).not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Abstract chunk is based on relations"
            )
            return self._get_abstract_chunk_from_relations()
        self.bubble_chamber.loggers["activity"].log("Abstract chunk is based on labels")
        return self._get_abstract_chunk_from_labels()

    def _get_abstract_chunk_from_correspondence(self):
        node_group = [
            group
            for group in self.targets["view"].node_groups
            if self.targets["projectee"] in group.values()
        ][0]
        return [node for node in node_group.values() if node.name is not None][0]

    def _get_abstract_chunk_from_relations(self):
        # TODO: further divide according to combination types of meaning concept
        relation = self.targets["projectee"].relations.get()
        relative = self.targets["projectee"].relatives.get()
        relative_correspondee = (
            relative.correspondences_to_space(self.targets["view"].output_space)
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

    def _get_abstract_chunk_from_labels(self):
        def _abstract_chunk_from_concepts(meaning_concept, grammar_concept):
            try:
                return (
                    meaning_concept.relations.where(parent_concept=grammar_concept)
                    .get(key=lambda x: x.end.activation)
                    .end
                )
            except MissingStructureError:
                root_letter_chunk = (
                    meaning_concept.root.relations.where(parent_concept=grammar_concept)
                    .get(key=lambda x: x.end.activation)
                    .end
                )
                self.bubble_chamber.loggers["activity"].log(
                    f"Root letter chunk: {root_letter_chunk}"
                )
                arg_letter_chunk = _abstract_chunk_from_concepts(
                    meaning_concept.args[0], grammar_concept
                )
                self.bubble_chamber.loggers["activity"].log(
                    f"Arg letter chunk: {arg_letter_chunk}"
                )
                return self.bubble_chamber.new_letter_chunk(
                    name=f"{root_letter_chunk.name} {arg_letter_chunk.name}",
                    locations=[
                        location.copy()
                        for location in meaning_concept.locations
                        + grammar_concept.locations
                    ],
                    parent_space=meaning_concept.parent_space,
                    parent_id=self.codelet_id,
                    left_branch=self.bubble_chamber.new_set(root_letter_chunk),
                    right_branch=self.bubble_chamber.new_set(arg_letter_chunk),
                    meaning_concept=meaning_concept,
                    grammar_concept=grammar_concept,
                )

        grammar_label = (
            self.targets["projectee"]
            .labels.filter(
                lambda x: x.parent_concept.parent_space
                == self.bubble_chamber.conceptual_spaces["grammar"]
            )
            .get()
        )
        self.bubble_chamber.loggers["activity"].log(f"Grammar label: {grammar_label}")
        grammar_concept = (
            grammar_label.parent_concept
            if not grammar_label.parent_concept.is_slot
            else grammar_label.parent_concept.non_slot_value
        )
        meaning_label = (
            self.targets["projectee"]
            .labels.filter(
                lambda x: x.parent_concept.parent_space
                != self.bubble_chamber.conceptual_spaces["grammar"]
            )
            .get()
        )
        self.bubble_chamber.loggers["activity"].log(f"Meaning label: {meaning_label}")
        meaning_concept = (
            meaning_label.parent_concept
            if not meaning_label.parent_concept.is_slot
            else meaning_label.parent_concept.non_slot_value
        )
        if meaning_concept is None:
            meaning_concept = meaning_label.parent_concept._non_slot_value = (
                meaning_label.parent_concept.parent_space.contents.where(
                    is_concept=True, is_compound_concept=False
                )
                .filter(
                    lambda x: all(
                        [
                            x.has_relation_with(
                                relation.arguments.excluding(
                                    meaning_label.parent_concept
                                )
                                .get()
                                .non_slot_value,
                                relation.parent_concept.non_slot_value,
                            )
                            for relation in meaning_label.parent_concept.relations
                        ]
                    )
                )
                .get(key=activation)
            )
        self.bubble_chamber.loggers["activity"].log(
            f"Meaning concept: {meaning_concept}"
        )
        return _abstract_chunk_from_concepts(meaning_concept, grammar_concept)
