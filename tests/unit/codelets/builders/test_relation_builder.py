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
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    chamber.concepts = {"relation": Mock(), "build": Mock()}
    relational_concept_space = Mock()
    relational_concept_space.contents.of_type.return_value = StructureCollection(
        {parent_concept}
    )
    relational_concept = Mock()
    relational_concept.child_spaces = StructureCollection({relational_concept_space})
    space = Mock()
    space.name = "relational concepts"
    space.contents.of_type.return_value = StructureCollection(
        {relational_concept_space}
    )
    chamber.spaces = StructureCollection({space})
    return chamber


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


@pytest.mark.skip
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
    assert hasinstance(relation_builder.child_structures, Relation)
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationEvaluator)


@pytest.mark.skip
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
