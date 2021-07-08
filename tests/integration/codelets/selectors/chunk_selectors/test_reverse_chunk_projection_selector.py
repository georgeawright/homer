import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors.chunk_selectors import ReverseChunkProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    chunk_concept = Concept(
        Mock(),
        Mock(),
        "chunk",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(chunk_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, select_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def good_chunk():
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({Mock()}),
        Mock(),
        1.0,
    )
    chunk._activation = 0.0
    return chunk


@pytest.fixture
def bad_chunk():
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({Mock()}),
        Mock(),
        0.0,
    )
    chunk._activation = 1.0
    return chunk


@pytest.mark.skip
def test_good_chunk_is_boosted(bubble_chamber, good_chunk):
    correspondence = Mock()
    correspondence.is_correspondence = True
    correspondence.parent_view = Mock()
    correspondence.quality = 1.0
    correspondence.activation = 1.0
    original_good_chunk_activation = good_chunk.activation
    parent_id = ""
    champion = good_chunk
    urgency = 1.0
    selector = ReverseChunkProjectionSelector.spawn(
        parent_id,
        bubble_chamber,
        StructureCollection({champion, correspondence}),
        urgency,
    )
    selector.run()
    good_chunk.update_activation()
    assert good_chunk.activation > original_good_chunk_activation


@pytest.mark.skip
def test_bad_chunk_is_boosted(bubble_chamber, bad_chunk):
    correspondence = Mock()
    correspondence.is_correspondence = True
    correspondence.parent_view = Mock()
    correspondence.quality = 1.0
    correspondence.activation = 1.0
    original_bad_chunk_activation = bad_chunk.activation
    parent_id = ""
    champion = bad_chunk
    urgency = 1.0
    selector = ReverseChunkProjectionSelector.spawn(
        parent_id,
        bubble_chamber,
        StructureCollection({champion, correspondence}),
        urgency,
    )
    selector.run()
    bad_chunk.update_activation()
    assert bad_chunk.activation <= original_bad_chunk_activation
