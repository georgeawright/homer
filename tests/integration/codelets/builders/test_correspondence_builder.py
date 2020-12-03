import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import DifferenceClassifier, ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Correspondence, Relation
from homer.structures.spaces import ConceptualSpace, Frame, WorkingSpace


@pytest.fixture
def more_concept():
    classifier = DifferenceClassifier(ProximityClassifier())
    comparison_space = ConceptualSpace(
        Mock(), Mock(), "comparison", StructureCollection(), Mock()
    )
    more = Concept(
        Mock(),
        Mock(),
        "more",
        [5],
        classifier,
        comparison_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    comparison_space.contents.add(more)
    return more


@pytest.fixture
def location_concept():
    concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    return concept


@pytest.fixture
def location_conceptual_space(location_concept):
    space = ConceptualSpace(
        Mock(), Mock(), "location", StructureCollection(), location_concept
    )
    return space


@pytest.fixture
def target_conceptual_space():
    temperature = Concept(
        Mock(),
        Mock(),
        "temperature",
        None,
        Mock(),
        Mock(),
        "value",
        StructureCollection(),
        math.dist,
    )
    temperature_space = ConceptualSpace(
        Mock(), Mock(), "temperature", StructureCollection(), temperature
    )
    return temperature_space


@pytest.fixture
def input_space(location_concept):
    space = WorkingSpace(
        Mock(), Mock(), "input", StructureCollection(), 0, location_concept
    )
    return space


@pytest.fixture
def active_frame():
    frame = Frame(Mock(), Mock(), "frame", StructureCollection(), Mock())
    return frame


@pytest.fixture
def bubble_chamber(
    more_concept,
    target_conceptual_space,
    input_space,
    active_frame,
    location_conceptual_space,
):
    working_spaces = StructureCollection({input_space, active_frame})
    correspondential_concepts_space = ConceptualSpace(
        Mock(),
        Mock(),
        "correspondential concepts",
        StructureCollection({more_concept}),
        Mock(),
    )
    labeling_spaces = ConceptualSpace(
        Mock(),
        Mock(),
        "label concepts",
        Mock(),
        Mock(),
        child_spaces=StructureCollection(
            {target_conceptual_space, location_conceptual_space}
        ),
    )
    chamber = BubbleChamber(
        StructureCollection(),
        working_spaces,
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    chamber.concepts.add(more_concept)
    chamber.conceptual_spaces.add(correspondential_concepts_space)
    chamber.conceptual_spaces.add(labeling_spaces)
    correspondence_concept = Concept(
        Mock(),
        Mock(),
        "correspondence",
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(correspondence_concept)
    build_concept = Concept(
        Mock(), Mock(), "build", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(build_concept)
    relation = Relation(
        Mock(), Mock(), correspondence_concept, build_concept, None, None, 1
    )
    correspondence_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber, target_conceptual_space, input_space, active_frame):
    parent_spaces = StructureCollection({input_space, target_conceptual_space})
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [5],
        Location([0, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    neighbouring_chunk = Chunk(
        Mock(),
        Mock(),
        [5],
        Location([1, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    bubble_chamber.chunks.add(neighbouring_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(neighbouring_chunk)
    active_frame.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    neighbouring_chunk.parent_spaces.add(input_space)
    second_chunk.parent_spaces.add(active_frame)
    chunk.parent_spaces.add(target_conceptual_space)
    second_chunk.parent_spaces.add(target_conceptual_space)
    return chunk


def test_successful_adds_correspondence_to_chunk_and_spawns_follow_up_and_same_correspondence_cannot_be_recreated(
    bubble_chamber, input_space, target_chunk
):
    parent_id = ""
    urgency = 1.0

    builder = CorrespondenceBuilder.spawn(
        parent_id, bubble_chamber, input_space, target_chunk, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Correspondence)
    assert isinstance(builder.child_codelets[0], CorrespondenceBuilder)
    builder = CorrespondenceBuilder.spawn(
        parent_id, bubble_chamber, input_space, target_chunk, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
