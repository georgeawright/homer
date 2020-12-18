import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import FunctionWordBuilder, WordBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunks import Word


@pytest.mark.skip
def test_successful_creates_word():
    with patch.object(Location, "for_correspondence_between", return_value=Mock()):
        bubble_chamber = Mock()
        bubble_chamber.concepts = {"word": Mock(), "build": Mock(), "same": Mock()}
        target_view = Mock()
        target_view.output_space.contents = StructureCollection()
        target_correspondence = Mock()
        target_correspondence.activation = 1.0
        word_builder = WordBuilder(
            Mock(), Mock(), bubble_chamber, target_view, target_correspondence, Mock()
        )
        result = word_builder.run()
        assert CodeletResult.SUCCESS == result
        assert isinstance(word_builder.child_structure, Word)
        assert 1 == len(word_builder.child_codelets)
        assert isinstance(word_builder.child_codelets[0], FunctionWordBuilder)
