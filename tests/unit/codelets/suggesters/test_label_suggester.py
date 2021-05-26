import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters import LabelSuggester
from homer.codelets.builders import LabelBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Concept
from homer.tools import hasinstance


@pytest.fixture
def working_space():
    space = Mock()
    space.parent_concept.relevant_value = "value"
    space.contents = StructureCollection()
    return space


@pytest.fixture
def parent_concept(working_space):
    concept = Mock()
    concept.relevant_value = "value"
    concept.parent_space.instance_in_space.return_value = working_space
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    chamber.concepts = {"label": Mock(), "suggest": Mock()}
    label_concept_space = Mock()
    label_concept_space.parent_concept.relevant_value = "value"
    label_concept_space.is_basic_level = True
    label_concept_space.instance_type = str
    label_concept_space.contents.of_type.return_value = StructureCollection(
        {parent_concept}
    )
    space = Mock()
    space.name = "label concepts"
    space.contents.of_type.return_value = StructureCollection({label_concept_space})
    chamber.spaces = StructureCollection({space})
    top_level_working_space = Mock()
    top_level_working_space.name = "top level working"
    chamber.spaces.add(top_level_working_space)
    return chamber


@pytest.fixture
def target_chunk():
    chunk = Mock()
    chunk.is_chunk = True
    chunk.is_word = False
    chunk.has_label.return_value = False
    chunk.nearby.get_unhappy.return_value = Mock()
    chunk.value = ""
    return chunk


def test_bottom_up_codelet_gets_a_concept(bubble_chamber, target_chunk):
    target_structures = {"target_node": target_chunk, "parent_concept": None}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    assert label_suggester.parent_concept is None
    label_suggester.run()
    assert label_suggester.parent_concept is not None


def test_gives_high_confidence_for_positive_example(bubble_chamber, target_chunk):
    target_structures = {"target_node": target_chunk, "parent_concept": None}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = label_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert label_suggester.confidence == 1
    assert len(label_suggester.child_codelets) == 1
    assert isinstance(label_suggester.child_codelets[0], LabelBuilder)


def test_gives_low_confidence_bad_example(bubble_chamber, target_chunk):
    parent_concept = Mock()
    parent_concept.classifier.classify.return_value = 0.0
    target_structures = {"target_node": target_chunk, "parent_concept": parent_concept}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = label_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert label_suggester.confidence == 0
    assert len(label_suggester.child_codelets) == 1
    assert isinstance(label_suggester.child_codelets[0], LabelBuilder)


def test_fizzles_when_label_exists(bubble_chamber, target_chunk):
    target_chunk.has_label.return_value = True
    target_structures = {"target_node": target_chunk, "parent_concept": None}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = label_suggester.run()
    assert CodeletResult.FIZZLE == result
