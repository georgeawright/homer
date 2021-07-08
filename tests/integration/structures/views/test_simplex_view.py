import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk
from homer.structures.spaces import Frame, WorkingSpace
from homer.structures.views import SimplexView


@pytest.mark.skip
def test_copy():
    working_input = WorkingSpace(
        "", "", "working_input", Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    working_temperature_space = WorkingSpace(
        "",
        "",
        "working_temperature",
        Mock(),
        Mock(),
        [Location([], working_input)],
        StructureCollection(),
        0,
        [],
        [],
    )
    working_chunk = Chunk(
        "",
        "",
        [Location([], working_input), Location([], working_temperature_space)],
        Mock(),
        working_input,
        Mock(),
    )
    working_input.add(working_chunk)
    working_label = Label(
        "", "", working_chunk, Mock(), working_temperature_space, Mock()
    )
    working_chunk.links_out.add(working_label)
    frame_input = Frame(
        "", "", "frame_input", Mock(), Mock(), [], StructureCollection()
    )
    frame_temperature_space = WorkingSpace(
        "",
        "",
        "frame_temperature",
        Mock(),
        Mock(),
        [Location([], frame_input)],
        StructureCollection(),
        0,
        [],
        [],
    )
    frame_chunk = Chunk(
        "",
        "",
        [Location([], frame_input), Location([], frame_temperature_space)],
        Mock(),
        working_input,
        Mock(),
    )
    frame_input.add(frame_chunk)
    frame_label = Label("", "", frame_chunk, Mock(), frame_temperature_space, Mock())
    frame_chunk.links_out.add(frame_label)
    view_output = WorkingSpace(
        "", "", "view_output", Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    view = SimplexView(
        "",
        "",
        Mock(),
        StructureCollection(),
        StructureCollection({working_input, frame_input}),
        view_output,
        Mock(),
    )
    chunks_correspondence = Correspondence(
        "",
        "",
        working_chunk,
        frame_chunk,
        working_temperature_space,
        frame_temperature_space,
        [
            Location([], working_temperature_space),
            Location([], frame_temperature_space),
        ],
        Mock(),
        Mock(),
        view,
        Mock(),
    )
    working_chunk.links_out.add(chunks_correspondence)
    working_chunk.links_in.add(chunks_correspondence)
    frame_chunk.links_out.add(chunks_correspondence)
    frame_chunk.links_in.add(chunks_correspondence)
    view.members.add(chunks_correspondence)
    labels_correspondence = Correspondence(
        "",
        "",
        working_label,
        frame_label,
        working_temperature_space,
        frame_temperature_space,
        [
            Location([], working_temperature_space),
            Location([], frame_temperature_space),
        ],
        Mock(),
        Mock(),
        view,
        Mock(),
    )
    working_label.links_out.add(labels_correspondence)
    working_label.links_in.add(labels_correspondence)
    frame_label.links_out.add(labels_correspondence)
    frame_label.links_in.add(labels_correspondence)
    view.members.add(labels_correspondence)
    bubble_chamber = Mock()
    replacement_chunk = Chunk(
        "",
        "",
        [Location([], working_input), Location([], working_temperature_space)],
        Mock(),
        working_input,
        Mock(),
    )
    copy = view.copy(
        bubble_chamber=bubble_chamber,
        parent_id="",
        original_structure=working_chunk,
        replacement_structure=replacement_chunk,
    )
    assert isinstance(copy, SimplexView)
    assert len(copy.members) == 2
