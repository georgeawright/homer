import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters.projection_suggesters import (
    RelationProjectionSuggester,
)
from linguoplotter.structure_collection import StructureCollection


@pytest.fixture
def target_view(bubble_chamber):
    view = Mock()
    view.slot_values = {}
    input_space = Mock()
    input_space.quality = 1
    view.input_spaces = bubble_chamber.new_structure_collection(input_space)
    return view


@pytest.fixture
def target_projectee(bubble_chamber, target_view):
    relation = Mock()
    relation.has_correspondence_to_space.return_value = False
    relation.start.has_correspondence_to_space.return_value = True
    relation.end.has_correspondence_to_space.return_value = True
    return relation


def test_suggests_projection_from_slot(bubble_chamber, target_view, target_projectee):
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = RelationProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FINISH == suggester.result


def test_gives_full_confidence_to_project_non_slot(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.correspondences = bubble_chamber.new_structure_collection()
    target_projectee.is_slot = False
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = RelationProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FINISH == suggester.result
    assert 1.0 == suggester.confidence


def test_fizzles_if_relation_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = RelationProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result


def test_fizzles_if_relation_start_has_no_correspondence_to_output(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.start.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = RelationProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
