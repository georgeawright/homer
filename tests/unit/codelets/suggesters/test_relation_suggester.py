import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import RelationBuilder
from homer.codelets.suggesters import RelationSuggester
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
    chamber.concepts = {"relation": Mock(), "suggest": Mock()}
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


def test_bottom_up_codelet_gets_a_concept(bubble_chamber):
    target_structures = {
        "target_space": Mock(),
        "target_structure_one": Mock(),
        "target_structure_two": None,
        "parent_concept": None,
    }
    relation_suggester = RelationSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    assert relation_suggester.parent_concept is None
    relation_suggester.run()
    assert relation_suggester.parent_concept is not None
    assert relation_suggester._target_structures["parent_concept"] is not None


def test_codelet_gets_a_second_target_structure(bubble_chamber, target_structure_one):
    target_structures = {
        "target_space": Mock(),
        "target_structure_one": target_structure_one,
        "target_structure_two": None,
        "parent_concept": None,
    }
    relation_suggester = RelationSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert relation_suggester.target_structure_two is None
    relation_suggester.run()
    assert relation_suggester.target_structure_two is not None
    assert relation_suggester._target_structures["target_structure_two"] is not None


def test_gives_high_confidence_for_good_example(
    bubble_chamber, parent_concept, target_structure_one
):
    target_structures = {
        "target_space": Mock(),
        "target_structure_one": target_structure_one,
        "target_structure_two": None,
        "parent_concept": parent_concept,
    }
    relation_suggester = RelationSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    result = relation_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert relation_suggester.confidence == 1
    assert len(relation_suggester.child_codelets) == 1
    assert isinstance(relation_suggester.child_codelets[0], RelationBuilder)


def test_gives_low_confidence_for_bad_example(
    parent_concept, bubble_chamber, target_structure_one
):
    target_structures = {
        "target_space": Mock(),
        "target_structure_one": target_structure_one,
        "target_structure_two": None,
        "parent_concept": parent_concept,
    }
    parent_concept.classifier.classify.return_value = 0.0
    relation_suggester = RelationSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = relation_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert relation_suggester.confidence == 0
    assert len(relation_suggester.child_codelets) == 1
    assert isinstance(relation_suggester.child_codelets[0], RelationBuilder)


def test_fizzles_when_relation_already_exists(bubble_chamber, target_structure_one):
    target_structures = {
        "target_space": Mock(),
        "target_structure_one": Mock(),
        "target_structure_two": None,
        "parent_concept": None,
    }
    target_structure_one.has_relation.return_value = True
    relation_suggester = RelationSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = relation_suggester.run()
    assert CodeletResult.FIZZLE == result