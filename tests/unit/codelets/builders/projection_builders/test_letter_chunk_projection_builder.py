import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.projection_builders import LetterChunkProjectionBuilder


def test_projects_non_slot_into_output(bubble_chamber):
    grammar_space = Mock()
    grammar_space.name = "grammar"
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(
        grammar_space
    )

    word_copy = Mock()
    word_copy.locations = []
    abstract_chunk = Mock()
    abstract_chunk.copy_to_location.return_value = word_copy

    target_projectee = Mock()
    target_projectee.is_slot = False
    target_projectee.abstract_chunk = abstract_chunk
    target_projectee.has_correspondence_to_space.return_value = False

    target_view = Mock()

    target_structures = {
        "target_projectee": target_projectee,
        "target_view": target_view,
    }

    projection_builder = LetterChunkProjectionBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    projection_builder.run()
    assert CodeletResult.FINISH == projection_builder.result
    assert word_copy in projection_builder.child_structures


def test_projects_correspondee_of_slot_into_output(bubble_chamber):
    grammar_space = Mock()
    grammar_space.name = "grammar"
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(
        grammar_space
    )

    abstract_chunk = Mock()
    abstract_chunk.locations = []
    abstract_chunk.left_branch = []
    abstract_chunk.right_branch = []
    abstract_chunk.super_chunks = []

    corresponding_word = Mock()
    corresponding_word.abstract_chunk = abstract_chunk

    target_projectee = Mock()
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = False
    target_projectee.correspondences.is_empty.return_value = False
    target_projectee.correspondees.get.return_value = corresponding_word

    target_view = Mock()

    target_structures = {
        "target_projectee": target_projectee,
        "target_view": target_view,
    }

    projection_builder = LetterChunkProjectionBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    projection_builder.run()
    assert CodeletResult.FINISH == projection_builder.result


def test_projects_slot_into_output_according_to_relation(bubble_chamber):
    grammar_space = Mock()
    grammar_space.name = "grammar"
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(
        grammar_space
    )

    abstract_chunk = Mock()
    abstract_chunk.locations = []
    abstract_chunk.left_branch = []
    abstract_chunk.right_branch = []
    abstract_chunk.super_chunks = []

    parent_concept = Mock()
    abstract_relation = Mock()
    abstract_relation.parent_concept = parent_concept
    abstract_relation.arguments.get.return_value = abstract_chunk
    abstract_relations = bubble_chamber.new_structure_collection(abstract_relation)
    relation = Mock()
    relation.parent_concept = parent_concept
    relative_correspondee = Mock()
    relative_correspondee.abstract_chunk.relations = abstract_relations
    relative_slot = Mock()
    relative_correspondence = Mock()
    relative_correspondence.end = relative_correspondee
    relative_slot.correspondences_to_space.return_value = (
        bubble_chamber.new_structure_collection(relative_correspondence)
    )
    abstract_relation.start = relative_correspondee.abstract_chunk

    target_projectee = Mock()
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = False
    target_projectee.correspondences.is_empty.return_value = True
    target_projectee.relations = bubble_chamber.new_structure_collection(relation)
    target_projectee.relatives.get.return_value = relative_slot

    target_view = Mock()

    target_structures = {
        "target_projectee": target_projectee,
        "target_view": target_view,
    }

    projection_builder = LetterChunkProjectionBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    projection_builder.run()
    assert CodeletResult.FINISH == projection_builder.result


def test_projects_slot_into_output_according_to_label(bubble_chamber):
    grammar_space = Mock()
    grammar_space.name = "grammar"
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(
        grammar_space
    )

    abstract_chunk = Mock()
    abstract_chunk.locations = []
    abstract_chunk.left_branch = []
    abstract_chunk.right_branch = []
    abstract_chunk.super_chunks = []

    grammar_concept = Mock()
    grammar_concept.is_slot = False
    meaning_relation = Mock()
    meaning_relation.parent_concept = grammar_concept
    meaning_relation.end = abstract_chunk
    meaning_relation.end.activation = 1.0
    meaning_relations = bubble_chamber.new_structure_collection(meaning_relation)
    meaning_concept = Mock()
    meaning_concept.is_slot = False
    meaning_concept.relations.where.return_value = meaning_relations
    grammar_label = Mock()
    grammar_label.parent_concept.relatives = bubble_chamber.new_structure_collection(
        grammar_concept
    )
    grammar_label.parent_concept.parent_space = grammar_space
    meaning_label = Mock()
    meaning_label.parent_concept.parent_space = Mock()
    meaning_label.parent_concept.relatives = bubble_chamber.new_structure_collection(
        meaning_concept
    )

    target_projectee = Mock()
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = False
    target_projectee.correspondences.is_empty.return_value = True
    target_projectee.relations.is_empty.return_value = True
    target_projectee.labels = bubble_chamber.new_structure_collection(
        grammar_label, meaning_label
    )

    target_view = Mock()

    target_structures = {
        "target_projectee": target_projectee,
        "target_view": target_view,
    }

    projection_builder = LetterChunkProjectionBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    projection_builder.run()
    assert CodeletResult.FINISH == projection_builder.result
