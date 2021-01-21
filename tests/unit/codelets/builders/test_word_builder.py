import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import FunctionWordBuilder, WordBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunks import Word


def test_successful_creates_word():
    with patch.object(Location, "for_correspondence_between", return_value=Mock()):
        bubble_chamber = Mock()
        bubble_chamber.concepts = {"word": Mock(), "build": Mock(), "same": Mock()}
        target_view = Mock()
        target_view.output_space.contents = StructureCollection()
        parent_concept = Mock()
        conceptual_space = Mock()
        conceptual_space.contents = [parent_concept]
        label = Mock()
        label.parent_concept = parent_concept
        start = Mock()
        start_space = Mock()
        start_space.conceptual_space = conceptual_space
        end = Mock()
        end.labels = StructureCollection({label})
        end_space = Mock()
        target_correspondence = Mock()
        target_correspondence.start = start
        target_correspondence.end = end
        target_correspondence.start_space = start_space
        target_correspondence.end_space = end_space
        target_correspondence.get_slot_argument.return_value = start
        target_correspondence.get_non_slot_argument.return_value = end
        target_correspondence.activation = 1.0
        word_builder = WordBuilder(
            Mock(), Mock(), bubble_chamber, target_view, target_correspondence, Mock()
        )
        result = word_builder.run()
        assert CodeletResult.SUCCESS == result
        assert isinstance(word_builder.child_structure, Word)
        assert 1 == len(word_builder.child_codelets)
        assert isinstance(word_builder.child_codelets[0], FunctionWordBuilder)
