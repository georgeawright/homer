from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import FunctionWordsBuilder, WordBuilder
from homer.structures.chunks import Word


def test_successful_creates_word():
    target_correspondence = Mock()
    target_correspondence.activation = 1.0
    word_builder = WordBuilder(
        Mock(), Mock(), Mock(), Mock(), target_correspondence, Mock()
    )
    result = word_builder.run()
    assert CodeletResult.SUCCESS == result
    assert 1 == len(word_builder.child_codelets)
    assert isinstance(word_builder.child_codelets[0], FunctionWordsBuilder)
