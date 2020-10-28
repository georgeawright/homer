from unittest.mock import Mock

from homer.codelets.builders import ProjectionBuilder
from homer.structure import Structure


def test_successful_creates_projection_and_spawns_follow_up():
    bubble_chamber = Mock()
    target_correspondence = Mock()
    projection_builder = ProjectionBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_correspondence, Mock()
    )
    projection_builder.run()
    assert isinstance(projection_builder.child_structure, Structure)
    assert len(projection_builder.child_codelets) == 1
    assert isinstance(projection_builder.child_codelets[0], ProjectionBuilder)


def test_fizzles_in_unsuitable_conditions():
    bubble_chamber = Mock()
    target_correspondence = Mock()
    projection_builder = ProjectionBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_correspondence, Mock()
    )
    projection_builder.run()
    assert projection_builder.child_structure is None
    assert len(projection_builder.child_codelets) == 1
    assert isinstance(projection_builder.child_codelets[0], ProjectionBuilder)
