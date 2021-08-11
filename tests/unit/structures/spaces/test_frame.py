from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.spaces import Frame


def test_instantiate():
    input_space = Mock()
    input_copy = Mock()
    input_space.copy.return_value = (input_copy, {})
    output_space = Mock()
    output_copy = Mock()
    output_space.copy.return_value = (output_copy, {})
    frame = Frame("", "", "", Mock(), StructureCollection(), input_space, output_space)

    instance = frame.instantiate(input_space, "", Mock())
    assert instance.input_space == input_copy
    assert instance.output_space == output_copy

    reverse_instance = frame.instantiate(output_space, "", Mock())
    assert reverse_instance.input_space == output_copy
    assert reverse_instance.output_space == input_copy
