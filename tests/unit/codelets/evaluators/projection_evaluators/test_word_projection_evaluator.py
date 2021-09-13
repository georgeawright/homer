import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.projection_evaluators import WordProjectionEvaluator
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, label_quality", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, label_quality):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "word": Mock()}
    concept = Mock()
    label = Mock()
    label.parent_concept = concept
    label.quality = label_quality
    chunk = Mock()
    chunk.labels = StructureCollection({label})
    word = Mock()
    word.is_word = True
    word.quality = current_quality
    word.concepts = StructureCollection({concept})
    word.correspondees = StructureCollection({chunk})
    evaluator = WordProjectionEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({word}), Mock()
    )
    evaluator.run()
    assert word.quality == label_quality


def test_gives_function_word_maximum_quality():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "word": Mock()}
    word = Mock()
    word.is_word = True
    word.quality = 0
    correspondee = Mock()
    correspondee.labels = StructureCollection()
    word.correspondees = StructureCollection({correspondee})
    evaluator = WordProjectionEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({word}), Mock()
    )
    evaluator.run()
    assert 1 == word.quality
