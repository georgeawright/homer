import pytest
from unittest.mock import Mock

from homer.codelets.suggesters import (
    CorrespondenceSuggester,
    LabelSuggester,
    PhraseSuggester,
    RelationSuggester,
)
from homer.codelets.factories import ConceptDrivenFactory
from homer.structure_collection import StructureCollection


@pytest.fixture
def concepts():
    suggest_concept = Mock()
    suggest_concept.name = "suggest"
    inner_concept = Mock()
    inner_concept.name = "inner"
    forward_concept = Mock()
    forward_concept.name = "forward"
    label_concept = Mock()
    label_concept.name = "label"
    relation_concept = Mock()
    relation_concept.name = "relation"
    correspondence_concept = Mock()
    correspondence_concept.name = "correspondence"
    phrase_concept = Mock()
    phrase_concept.name = "phrase"
    concepts = StructureCollection(
        {
            suggest_concept,
            inner_concept,
            forward_concept,
            label_concept,
            relation_concept,
            correspondence_concept,
            phrase_concept,
        }
    )
    for concept in concepts:
        concept.activation = 0.5
    return concepts


@pytest.fixture
def example_label_concept():
    concept = Mock()
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def example_correspondence_concept():
    concept = Mock()
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def example_relation_concept():
    concept = Mock()
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def example_rule():
    rule = Mock()
    rule.activation = 1.0
    return rule


@pytest.fixture
def bubble_chamber(
    concepts,
    example_correspondence_concept,
    example_label_concept,
    example_relation_concept,
    example_rule,
):
    chamber = Mock()
    chamber.concepts = concepts
    input_node = Mock()
    input_node.value = ""
    chamber.input_nodes = StructureCollection({input_node})

    correspondence_space = Mock()
    correspondence_space.name = "correspondence space"
    correspondence_space.contents.of_type.return_value = StructureCollection(
        {example_correspondence_concept}
    )
    correspondential_concepts = Mock()
    correspondential_concepts.name = "correspondential concepts"
    correspondential_concepts.contents.of_type.return_value = StructureCollection(
        {correspondence_space}
    )

    label_space = Mock()
    label_space.contents.of_type.return_value = StructureCollection(
        {example_label_concept}
    )
    label_concepts = Mock()
    label_concepts.name = "label concepts"
    label_concepts.contents.of_type.return_value = StructureCollection({label_space})

    relation_space = Mock()
    relation_space.name = "relation space"
    relation_space.contents.of_type.return_value = StructureCollection(
        {example_relation_concept}
    )
    relational_concepts = Mock()
    relational_concepts.name = "relational concepts"
    relational_concepts.contents.of_type.return_value = StructureCollection(
        {relation_space}
    )

    chamber.spaces = StructureCollection(
        {
            correspondence_space,
            correspondential_concepts,
            label_space,
            label_concepts,
            relation_space,
            relational_concepts,
        }
    )
    chamber.rules = StructureCollection({example_rule})
    chamber.satisfaction = 0
    return chamber


@pytest.fixture
def coderack():
    rack = Mock()
    rack.number_of_codelets_of_type.return_value = 0.0
    return rack


def test_gets_appropriate_follow_up_class(
    bubble_chamber,
    coderack,
    example_correspondence_concept,
    example_label_concept,
    example_relation_concept,
    example_rule,
):
    factory_codelet = ConceptDrivenFactory(
        Mock(), Mock(), bubble_chamber, coderack, Mock()
    )
    assert (
        factory_codelet._get_follow_up_class(example_correspondence_concept)
        == CorrespondenceSuggester
    )
    assert factory_codelet._get_follow_up_class(example_label_concept) == LabelSuggester
    assert (
        factory_codelet._get_follow_up_class(example_relation_concept)
        == RelationSuggester
    )
    assert factory_codelet._get_follow_up_class(example_rule) == PhraseSuggester
