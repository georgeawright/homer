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
def parent_concept():
    concept = Mock()
    concept.is_concept = True
    concept.structure_type = Label
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def conceptual_space(bubble_chamber, parent_concept):
    space = Mock()
    space.contents = StructureCollection({parent_concept})
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(
        conceptual_space
    )
    return space


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


def test_gives_high_confidence_for_positive_example(
    bubble_chamber, target_chunk, parent_concept
):
    target_structures = {"target_node": target_chunk, "parent_concept": parent_concept}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = label_suggester.run()
    assert CodeletResult.FINISH == result
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
    assert CodeletResult.FINISH == result
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
