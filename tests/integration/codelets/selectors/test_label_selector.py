import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors import LabelSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Label
from homer.structures.spaces import ConceptualSpace, WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    return chamber


@pytest.fixture
def conceptual_space():
    space = ConceptualSpace(Mock(), Mock(), Mock(), Mock(), Mock())
    return space


@pytest.fixture
def working_space():
    space = WorkingSpace(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock())
    return space


@pytest.fixture
def chunk(working_space):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({working_space}),
    )
    return chunk


@pytest.fixture
def good_label(chunk, conceptual_space, working_space):
    concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), conceptual_space, Mock(), Mock(), Mock()
    )
    label = Label(
        Mock(),
        Mock(),
        chunk,
        concept,
        working_space,
        1.0,
    )
    chunk.links_out.add(label)
    working_space.contents.add(label)
    return label


@pytest.fixture
def bad_label(chunk, conceptual_space, working_space):
    concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), conceptual_space, Mock(), Mock(), Mock()
    )
    label = Label(
        Mock(),
        Mock(),
        chunk,
        concept,
        working_space,
        0.0,
    )
    chunk.links_out.add(label)
    working_space.contents.add(label)
    return label


def test_good_chunk_is_boosted_bad_chunk_is_decayed(
    bubble_chamber, good_label, bad_label
):
    parent_id = ""
    champion = bad_label
    urgency = 1.0
    selector = LabelSelector.spawn(parent_id, bubble_chamber, champion, urgency)
    for _ in range(20):
        selector.run()
        selector = selector.child_codelets[0]
        good_label.update_activation()
        bad_label.update_activation()
    assert 1 == good_label.activation
    assert 0 == bad_label.activation
