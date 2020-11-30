from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import FunctionWordBuilder
from homer.structure_collection import StructureCollection
from homer.structures.chunks import Word


def test_successful_creates_word():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"same": Mock(), "word": Mock(), "build": Mock()}
    bubble_chamber.spaces = {"text": Mock()}
    template = Mock()
    output_space = Mock()
    output_space.contents = StructureCollection()
    function_word_builder = FunctionWordBuilder(
        Mock(), Mock(), bubble_chamber, template, output_space, Mock()
    )
    result = function_word_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(function_word_builder.child_structure, Word)
    assert 1 == len(function_word_builder.child_codelets)
    assert isinstance(function_word_builder.child_codelets[0], FunctionWordBuilder)
