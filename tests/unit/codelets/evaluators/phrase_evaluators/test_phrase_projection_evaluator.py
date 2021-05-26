import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.phrase_evaluators import PhraseProjectionEvaluator
from homer.codelets.selectors.phrase_selectors import PhraseProjectionSelector
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "phrase": Mock()}

    view = Mock()
    input_phrase = Mock()
    frame_phrase = Mock()
    output_phrase = Mock()
    output_phrase.quality = current_quality

    input_to_output_correspondence = Mock()
    input_to_output_correspondence.is_correspondence = True
    input_to_output_correspondence.parent_view = view
    input_to_output_correspondence.start = input_phrase
    input_to_output_correspondence.quality = current_quality

    frame_to_output_correspondence = Mock()
    frame_to_output_correspondence.is_correspondence = True
    frame_to_output_correspondence.parent_view = view
    frame_to_output_correspondence.start = frame_phrase
    frame_to_output_correspondence.quality = current_quality

    input_to_frame_correspondence = Mock()
    input_to_frame_correspondence.parent_view = view
    input_to_frame_correspondence.quality = classification
    input_phrase.correspondences_with.return_value = StructureCollection(
        {input_to_frame_correspondence}
    )
    frame_phrase.correspondences_with.return_value = StructureCollection(
        {input_to_frame_correspondence}
    )

    evaluator = PhraseProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection(
            {
                input_to_output_correspondence,
                frame_to_output_correspondence,
                output_phrase,
            }
        ),
        Mock(),
    )
    evaluator.run()
    assert classification == output_phrase.quality
    assert classification == input_to_output_correspondence.quality
    assert classification == frame_to_output_correspondence.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseProjectionSelector)
