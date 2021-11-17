from unittest.mock import Mock

from homer.structures.spaces import Frame


def test_instantiate():
    input_space = Mock()
    input_copy = Mock()
    input_space.copy.return_value = (input_copy, {})
    output_space = Mock()
    output_copy = Mock()
    output_space.copy.return_value = (output_copy, {})
    frame = Frame(
        "", "", "", Mock(), [], input_space, output_space, Mock(), Mock(), Mock()
    )

    bubble_chamber = Mock()
    bubble_chamber.new_structure_collection.return_value = []

    instance = frame.instantiate(input_space, "", bubble_chamber)
    assert instance.input_space == input_copy
    assert instance.output_space == output_copy

    reverse_instance = frame.instantiate(output_space, "", bubble_chamber)
    assert reverse_instance.input_space == output_copy
    assert reverse_instance.output_space == input_copy
