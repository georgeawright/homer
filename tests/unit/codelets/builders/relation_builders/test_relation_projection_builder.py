import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.relation_builders import RelationProjectionBuilder
from homer.codelets.evaluators.relation_evaluators import RelationProjectionEvaluator
from homer.structure_collection import StructureCollection


@pytest.fixture
def target_view():
    view = Mock()
    existing_correspondence = Mock()
    existing_correspondence.name = "existing correspondence"
    existing_chunk = Mock()
    existing_word = Mock()
    existing_correspondence.arguments = StructureCollection(
        {existing_chunk, existing_word}
    )
    potential_relating_word = Mock()
    potential_relating_word.has_correspondence_to_space.return_value = False
    existing_word.potential_relating_words = StructureCollection(
        {potential_relating_word}
    )
    existing_correspondence.arguments = StructureCollection(
        {existing_chunk, existing_word}
    )
    existing_chunk.correspondences_to_space.return_value = StructureCollection(
        {existing_correspondence}
    )
    view.interpretation_space.contents.of_type.return_value = StructureCollection(
        {existing_chunk}
    )
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {
        "build": Mock(),
        "relation": Mock(),
        "noun": Mock(),
        "same": Mock(),
        "text": Mock(),
    }
    chamber.monitoring_views = StructureCollection({target_view})
    return chamber


@pytest.fixture
def parent_concept(bubble_chamber):
    concept = Mock()
    concept.value = [[4]]
    relational_space = Mock()
    relational_space.contents.of_type.return_value = StructureCollection({concept})
    relational_concepts = Mock()
    relational_concepts.contents.of_type.return_value = StructureCollection(
        {relational_space}
    )
    bubble_chamber.spaces = {"relational concepts": relational_concepts}
    return concept


@pytest.fixture
def target_structure_two():
    structure = Mock()
    structure.value = [[1]]
    return structure


@pytest.fixture
def target_space():
    space = Mock()
    space.contents = StructureCollection()
    space.parent_concept.value = [[4]]
    space.parent_concept.relevant_value = "value"
    return space


@pytest.fixture
def conceptual_space(target_space):
    space = Mock()
    space.instance_in_space.return_value = target_space
    space.no_of_dimensions = 1
    return space


@pytest.fixture
def target_word(bubble_chamber, parent_concept, conceptual_space):
    word = Mock()
    word_concept = Mock()
    link = Mock()
    link.activation = 1
    word_concept.relations_with.return_value = StructureCollection({link})
    word.lexeme.concepts.get_random.return_value = word_concept
    word_concept.parent_spaces = StructureCollection({conceptual_space})
    return word


def test_successful_creates_relation_corresponding_to_word_and_spawns_follow_up(
    bubble_chamber,
    target_view,
    target_word,
    target_structure_two,
    target_space,
    parent_concept,
):
    target_structure_one = Mock()
    target_structure_one.value = [[10]]
    target_structure_one.has_relation.return_value = False
    target_word.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_word": target_word,
        "parent_concept": parent_concept,
        "target_space": target_space,
    }
    builder = RelationProjectionBuilder("", "", bubble_chamber, target_structures, 1)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert len(builder.child_codelets) == 1
    assert isinstance(builder.child_codelets[0], RelationProjectionEvaluator)


def test_fizzles_if_target_word_already_has_correspondence_in_interpretation(
    bubble_chamber,
    target_view,
    target_word,
    target_structure_two,
    target_space,
    parent_concept,
):
    target_structure_one = Mock()
    target_structure_one.value = [[10]]
    target_structure_one.has_label.return_value = False
    target_word.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_word": target_word,
        "parent_concept": parent_concept,
        "target_space": target_space,
    }
    builder = RelationProjectionBuilder("", "", bubble_chamber, target_structures, 1)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result


def test_fizzles_if_target_chunk_already_has_corresponding_relation(
    bubble_chamber,
    target_view,
    target_word,
    target_structure_two,
    target_space,
    parent_concept,
):
    target_structure_one = Mock()
    target_structure_one.value = [[10]]
    target_structure_one.has_relation.return_value = True
    target_word.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_word": target_word,
        "parent_concept": parent_concept,
        "target_space": target_space,
    }
    builder = RelationProjectionBuilder("", "", bubble_chamber, target_structures, 1)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
