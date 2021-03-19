import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import PhraseEvaluator
from homer.codelets.selectors import PhraseSelector
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, new_quality", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, new_quality):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "phrase": Mock()}
    phrase = Mock()
    phrase.quality = current_quality
    phrase.left_branch.quality = new_quality
    phrase.right_branch.quality = new_quality
    phrase.rule.activation = new_quality
    phrase.unchunkedness = new_quality
    phrase.size = new_quality
    evaluator = PhraseEvaluator(Mock(), Mock(), bubble_chamber, phrase, Mock())
    evaluator.run()
    assert phrase.quality == new_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseSelector)
