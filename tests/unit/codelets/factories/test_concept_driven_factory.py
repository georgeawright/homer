import pytest
from unittest.mock import Mock

from homer.codelets.factories import ConceptDrivenFactory
from homer.structure_collection import StructureCollection


@pytest.fixture
def build_concept():
    concept = Mock()
    concept.name = "build"
    return concept


@pytest.fixture
def label_concept():
    concept = Mock()
    concept.name = "label"
    return concept


@pytest.fixture
def example_label_concept():
    concept = Mock()
    concept.name = "example"
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def bubble_chamber(
    build_concept,
    label_concept,
    example_label_concept,
):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {
        "build": build_concept,
        "label": label_concept,
    }
    input_node = Mock()
    input_node.value = ""
    bubble_chamber.input_nodes = StructureCollection({input_node})
    build_label_link = Mock()
    build_label_link.end = label_concept
    build_concept.links_out = StructureCollection({build_label_link})
    activities = Mock()
    activities.name = "activities"
    activities.contents = StructureCollection({build_concept})
    structures = Mock()
    structures.name = "structures"
    structures.contents = StructureCollection({label_concept})
    label_space = Mock()
    label_space.contents.of_type.return_value = StructureCollection(
        {example_label_concept}
    )
    label_space.name = "label space"
    label_spaces = Mock()
    label_spaces.name = "label spaces"
    label_spaces.where.return_value = label_spaces
    label_spaces.get_active.return_value = label_space
    label_concepts = Mock()
    label_concepts.name = "label concepts"
    label_concepts.contents.of_type.return_value = label_spaces
    bubble_chamber.spaces = StructureCollection(
        {activities, structures, label_concepts}
    )
    bubble_chamber.satisfaction = 0
    return bubble_chamber


@pytest.fixture
def coderack():
    rack = Mock()
    rack.number_of_codelets_of_type.return_value = 0.0
    return rack


def test_engenders_two_follow_ups(bubble_chamber, coderack):
    factory_codelet = ConceptDrivenFactory(
        Mock(), Mock(), bubble_chamber, coderack, Mock()
    )
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
