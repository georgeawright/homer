import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelBuilder
from homer.structure_collection import StructureCollection
from homer.structures import Concept
from homer.structures.links import Label


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.parent_space.instance.contents = StructureCollection()
    concept.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    chamber.concepts = {"label": Mock()}
    chamber.get_random_workspace_concept.return_value = parent_concept
    return chamber


@pytest.fixture
def target_chunk():
    chunk = Mock()
    chunk.has_label.return_value = False
    chunk.nearby.get_unhappy.return_value = Mock()
    return chunk


def test_bottom_up_codelet_gets_a_concept(bubble_chamber):
    target_chunk = Mock()
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    assert label_builder.parent_concept is None
    label_builder.run()
    assert label_builder.parent_concept is not None


def test_successful_creates_label_and_spawns_follow_up(bubble_chamber, target_chunk):
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    result = label_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(label_builder.child_structure, Label)
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)


def test_fails_when_chunk_is_bad_example(bubble_chamber, target_chunk):
    parent_concept = Mock()
    parent_concept.classify.return_value = 0.0
    label_builder = LabelBuilder(
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber,
        target_chunk,
        Mock(),
        parent_concept=parent_concept,
    )
    result = label_builder.run()
    assert CodeletResult.FAIL == result
    assert label_builder.child_structure is None
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)


def test_fizzles_when_label_exists(bubble_chamber, target_chunk):
    target_chunk.has_label.return_value = True
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    result = label_builder.run()
    assert CodeletResult.FIZZLE == result
    assert label_builder.child_structure is None
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)
