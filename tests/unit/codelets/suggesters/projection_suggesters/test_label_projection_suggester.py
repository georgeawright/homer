import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters.projection_suggesters import (
    LabelProjectionSuggester,
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
    label = Mock()
    label.start.has_correspondence_to_space.return_value = True
    return label


def test_gives_suggests_projection_from_slot(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FINISH == suggester.result


def test_fizzles_if_label_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_view.slot_values[target_projectee.structure_id] = Mock()
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result


def test_fizzles_if_label_start_has_no_correspondence_to_output(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.start.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
