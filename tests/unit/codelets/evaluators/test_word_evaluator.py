import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import WordEvaluator
from homer.codelets.selectors import WordSelector
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
    word.quality = current_quality
    word.concepts = StructureCollection({concept})
    word.correspondees = StructureCollection({chunk})
    evaluator = WordEvaluator(Mock(), Mock(), bubble_chamber, word, Mock())
    evaluator.run()
    assert word.quality == label_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], WordSelector)


def test_gives_function_word_maximum_quality():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "word": Mock()}
    word = Mock()
    word.quality = 0
    correspondee = Mock()
    correspondee.labels = StructureCollection()
    word.correspondees = StructureCollection({correspondee})
    evaluator = WordEvaluator(Mock(), Mock(), bubble_chamber, word, Mock())
    evaluator.run()
    assert 1 == word.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], WordSelector)
