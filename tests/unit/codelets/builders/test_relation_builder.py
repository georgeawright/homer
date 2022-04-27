import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.builders import ChunkBuilder, RelationBuilder
from linguoplotter.codelets.evaluators import RelationEvaluator
from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Relation
from linguoplotter.tools import hasinstance


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.location_in_space.return_value = Location([[10]], Mock())
    concept.proximity_to.return_value = 1.0
    return concept


@pytest.fixture
def target_structure_two():
    structure = Mock()
    location = Mock()
    location.coordinates = [[1]]
    structure.location_in_space.return_value = location
    return structure


@pytest.fixture
def target_structure_one(target_structure_two):
    structure = Mock()
    parent_space_contents = Mock()
    parent_space_contents.get_exigent.return_value = target_structure_two
    structure.parent_spaces.get_random.return_value = parent_space_contents
    structure.has_relation.return_value = False
    structure.nearby.get_unhappy.return_value = Mock()
    location = Mock()
    location.coordinates = [[10]]
    structure.location_in_space.return_value = location
    return structure


def test_successful_creates_relation_and_spawns_follow_up(
    bubble_chamber, target_structure_one, target_structure_two, parent_concept
):
    bubble_chamber.conceptual_spaces = {"magnitude": Mock()}
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
    assert CodeletResult.FINISH == result
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
