import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder
from homer.codelets.selectors import WordSelector
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"word": Mock(), "select": Mock()}
    return chamber


def test_word_is_boosted_follow_up_is_spawned(bubble_chamber):
    word = Mock()
    word.size = 1
    word.quality = 1.0
    word.activation = 0.0
    selector = WordSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        word,
        Mock(),
    )
    selector.run()
    assert CodeletResult.SUCCESS == selector.result
    assert word.boost_activation.is_called()
    assert 2 == len(selector.child_codelets)
    assert hasinstance(selector.child_codelets, WordBuilder)
    assert hasinstance(selector.child_codelets, WordSelector)
