import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder, RelationBuilder
from homer.codelets.evaluators import RelationEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.tools import hasinstance


@pytest.fixture
def parent_concept():
    concept = Mock()
    return concept


@pytest.fixture
def target_structure_two():
    structure = Mock()
    return structure


@pytest.fixture
def target_structure_one(target_structure_two):
    structure = Mock()
    parent_space_contents = Mock()
    parent_space_contents.get_exigent.return_value = target_structure_two
    structure.parent_spaces.get_random.return_value = parent_space_contents
    structure.has_relation.return_value = False
    structure.nearby.get_unhappy.return_value = Mock()
    return structure


def test_successful_creates_chunk_and_spawns_follow_up(
    bubble_chamber, target_structure_one, target_structure_two, parent_concept
):
    target_structures = {
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_space": Mock(),
        "parent_concept": parent_concept,
    }
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    result = relation_builder.run()
    assert CodeletResult.SUCCESS == result
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationEvaluator)


def test_fizzles_when_relation_already_exists(
    bubble_chamber, target_structure_one, target_structure_two, parent_concept
):
    target_structure_one.has_relation.return_value = True
    target_structures = {
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_space": Mock(),
        "parent_concept": parent_concept,
    }
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = relation_builder.run()
    assert CodeletResult.FIZZLE == result
    assert relation_builder.child_structures is None
