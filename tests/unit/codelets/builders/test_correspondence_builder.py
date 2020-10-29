import pytest
from unittest.mock import Mock

from homer.codelets.builders import CorrespondenceBuilder
from homer.structure import Structure
from homer.structures.links import Correspondence


@pytest.mark.skip
def test_successful_creates_chunk_and_spawns_follow_up():
    bubble_chamber = Mock()
    target_structure = Mock()
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure, Mock()
    )
    correspondence_builder.run()
    assert isinstance(correspondence_builder.child_structure, Correspondence)
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)


@pytest.mark.skip
def test_fails_when_chunks_do_not_correspond():
    bubble_chamber = Mock()
    target_structure = Mock()
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure, Mock()
    )
    correspondence_builder.run()
    assert correspondence_builder.child_structure is None
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)


@pytest.mark.skip
def test_fizzles_in_unsuitable_conditions():
    bubble_chamber = Mock()
    target_structure = Mock()
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure, Mock()
    )
    correspondence_builder.run()
    assert correspondence_builder.child_structure is None
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)
