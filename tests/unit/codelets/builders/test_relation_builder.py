import pytest
from unittest.mock import Mock

from homer.codelets.builders import RelationBuilder
from homer.structures.links import Relation


@pytest.mark.skip
def test_successful_creates_chunk_and_spawns_follow_up():
    bubble_chamber = Mock()
    target_structure = Mock()
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure, Mock()
    )
    relation_builder.run()
    assert isinstance(relation_builder.child_structure, Relation)
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationBuilder)


@pytest.mark.skip
def test_fails_when_structures_cannot_be_related():
    bubble_chamber = Mock()
    target_structure = Mock()
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure, Mock()
    )
    relation_builder.run()
    assert relation_builder.child_structure is None
    assert len(relation_builder.child_codelets) == 1
    # assert isinstance(relation_builder.child_codelets[0], RelationBuilder)


@pytest.mark.skip
def test_fizzles_in_unsuitable_conditions():
    bubble_chamber = Mock()
    target_structure = Mock()
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure, Mock()
    )
    relation_builder.run()
    assert relation_builder.child_structure is None
    assert len(relation_builder.child_codelets) == 1
    # should probably spawn chunk builder, ideally builder of the thing it was looking for?
    # assert isinstance(relation_builder.child_codelets[0], RelationBuilder)
