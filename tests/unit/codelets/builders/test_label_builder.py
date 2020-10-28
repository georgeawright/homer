from unittest.mock import Mock

from homer.codelets.builders import LabelBuilder
from homer.structures import Concept
from homer.structures.links import Label


def test_bottom_up_codelet_gets_a_concept():
    bubble_chamber = Mock()
    target_chunk = Mock()
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    label_builder.run()
    assert isinstance(label_builder.parent_concept, Concept)


def test_successful_creates_label_and_spawns_follow_up():
    bubble_chamber = Mock()
    target_chunk = Mock()
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    label_builder.run()
    assert isinstance(label_builder.child_structure, Label)
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)


def test_fails_when_chunk_is_bad_example():
    bubble_chamber = Mock()
    target_chunk = Mock()
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    label_builder.run()
    assert label_builder.child_structure is None
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)


def test_fizzles_when_label_exists():
    bubble_chamber = Mock()
    target_chunk = Mock()
    label_builder = LabelBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    label_builder.run()
    assert label_builder.child_structure is None
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)
