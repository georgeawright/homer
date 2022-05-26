import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.builders import RelationBuilder
from linguoplotter.codelets.suggesters import RelationSuggester
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Relation
from linguoplotter.tools import hasinstance


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.is_concept = True
    concept.structure_type = Relation
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def conceptual_space(bubble_chamber, parent_concept):
    space = Mock()
    space.contents = bubble_chamber.new_structure_collection(parent_concept)
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(space)
    return space


@pytest.fixture
def target_structure_two():
    structure = Mock()
    structure.quality = 1.0
    return structure


@pytest.fixture
def target_structure_one(target_structure_two):
    structure = Mock()
    structure.quality = 1.0
    structure.get_potential_relative.return_value = target_structure_two
    return structure


def test_bottom_up_codelet_gets_a_concept(bubble_chamber, target_structure_one):
    target_structures = {
        "target_space": Mock(),
        "target_structure_one": target_structure_one,
        "target_structure_two": None,
        "parent_concept": None,
    }
    relation_suggester = RelationSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    assert relation_suggester.parent_concept is None
    try:
        relation_suggester.run()
    except TypeError:
        pass
    assert relation_suggester.parent_concept is not None


def test_codelet_gets_a_second_target_structure(
    bubble_chamber, target_structure_one, parent_concept
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
    assert relation_suggester.target_structure_two is None
    relation_suggester.run()
    assert relation_suggester.target_structure_two is not None


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
    assert CodeletResult.FINISH == result
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
    assert CodeletResult.FINISH == result
    assert relation_suggester.confidence == 0
    assert len(relation_suggester.child_codelets) == 1
    assert isinstance(relation_suggester.child_codelets[0], RelationBuilder)
