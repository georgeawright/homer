import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters import LabelSuggester
from linguoplotter.codelets.builders import LabelBuilder
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Concept
from linguoplotter.tools import hasinstance


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
    chunk.quality = 1.0
    return chunk


def test_bottom_up_codelet_gets_a_concept(bubble_chamber, target_chunk):
    target_structures = {"target_node": target_chunk, "parent_concept": None}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    assert label_suggester.parent_concept is None
    try:
        label_suggester.run()
    except TypeError:
        pass
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
    labels_where = Mock()
    labels_where.is_empty.return_value = False
    target_chunk.labels.where.return_value = labels_where
    target_structures = {"target_node": target_chunk, "parent_concept": None}
    label_suggester = LabelSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = label_suggester.run()
    assert CodeletResult.FIZZLE == result
