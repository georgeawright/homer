import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import LabelSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.tools import centroid_euclidean_distance


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    label_concept = Concept(
        Mock(),
        Mock(),
        "label",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(label_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), label_concept, select_concept, None, None, 1)
    label_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def conceptual_space():
    parent_concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
        distance_to_proximity_weight=1.5,
    )
    space = ConceptualSpace(
        Mock(), Mock(), Mock(), parent_concept, [], Mock(), 1, [], []
    )
    return space


@pytest.fixture
def working_space():
    parent_concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
        distance_to_proximity_weight=1.5,
    )
    space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        parent_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def chunk(bubble_chamber, working_space):
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[1, 1]], working_space)],
        Mock(),
        Mock(),
        Mock(),
    )
    working_space.add(chunk)
    bubble_chamber.chunks.add(chunk)
    nearby_chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0, 1]], working_space)],
        Mock(),
        Mock(),
        Mock(),
    )
    working_space.add(nearby_chunk)
    bubble_chamber.chunks.add(nearby_chunk)
    return chunk


@pytest.fixture
def good_label(chunk, conceptual_space, working_space):
    concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Location(Mock(), conceptual_space),
        Mock(),
        Mock(),
        conceptual_space,
        Mock(),
        Mock(),
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
        Mock(),
        Mock(),
        Mock(),
        Location(Mock(), conceptual_space),
        Mock(),
        Mock(),
        conceptual_space,
        Mock(),
        Mock(),
    )
    label = Label(
        Mock(),
        Mock(),
        chunk,
        concept,
        working_space,
        0.0,
    )
    label._activation = 1.0
    chunk.links_out.add(label)
    working_space.contents.add(label)
    return label


@pytest.mark.skip
def test_good_label_is_boosted_bad_label_is_decayed(
    bubble_chamber, good_label, bad_label
):
    original_good_label_activation = good_label.activation
    original_bad_label_activation = bad_label.activation
    parent_id = ""
    champion = bad_label
    urgency = 1.0
    selector = LabelSelector.spawn(
        parent_id, bubble_chamber, StructureCollection({champion}), urgency
    )
    selector.run()
    good_label.update_activation()
    bad_label.update_activation()
    assert good_label.activation > original_good_label_activation
    assert bad_label.activation < original_bad_label_activation
