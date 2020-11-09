import pytest
from unittest.mock import Mock

from homer.codelets import FactoryCodelet
from homer.codelets.builders import (
    ChunkBuilder,
    CorrespondenceBuilder,
    LabelBuilder,
    RelationBuilder,
    ViewBuilder,
    WordBuilder,
)
from homer.structure_collection import StructureCollection


@pytest.fixture
def builder_concept():
    return Mock()


@pytest.fixture
def evaluator_concept():
    return Mock()


@pytest.fixture
def selector_concept():
    return Mock()


@pytest.fixture
def chunk_concept():
    return Mock()


@pytest.fixture
def correspondence_concept():
    return Mock()


@pytest.fixture
def label_concept():
    return Mock()


@pytest.fixture
def relation_concept():
    return Mock()


@pytest.fixture
def view_concept():
    return Mock()


@pytest.fixture
def word_concept():
    return Mock()


@pytest.fixture
def bubble_chamber(
    builder_concept,
    evaluator_concept,
    selector_concept,
    chunk_concept,
    correspondence_concept,
    label_concept,
    relation_concept,
    view_concept,
    word_concept,
):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {
        "actions": Mock(),
        "structures": Mock(),
        "builder": builder_concept,
        "evaluator": evaluator_concept,
        "selector": selector_concept,
        "chunk": chunk_concept,
        "correspondence": correspondence_concept,
        "label": label_concept,
        "relation": relation_concept,
        "view": view_concept,
        "word": word_concept,
    }
    bubble_chamber.chunks = StructureCollection({Mock()})
    bubble_chamber.correspondences = StructureCollection({Mock()})
    bubble_chamber.labels = StructureCollection({Mock()})
    bubble_chamber.relations = StructureCollection({Mock()})
    bubble_chamber.views = StructureCollection({Mock()})
    space = Mock()
    space.chunks = StructureCollection({Mock()})
    space.labels = StructureCollection({Mock()})
    space.relations = StructureCollection({Mock()})
    bubble_chamber.spaces = StructureCollection({space})
    return bubble_chamber


def test_engenders_chunk_builder(bubble_chamber, builder_concept, chunk_concept):
    bubble_chamber.concepts["actions"].get_active.return_value = builder_concept
    bubble_chamber.concepts["structures"].get_active.return_value = chunk_concept
    factory_codelet = FactoryCodelet(Mock(), Mock(), bubble_chamber, Mock())
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
    assert isinstance(factory_codelet.child_codelets[0], ChunkBuilder) or isinstance(
        factory_codelet.child_codelets[1], ChunkBuilder
    )
    assert isinstance(factory_codelet.child_codelets[0], FactoryCodelet) or isinstance(
        factory_codelet.child_codelets[1], FactoryCodelet
    )


def test_engenders_correspondence_builder(
    bubble_chamber, builder_concept, correspondence_concept
):
    bubble_chamber.concepts["actions"].get_active.return_value = builder_concept
    bubble_chamber.concepts[
        "structures"
    ].get_active.return_value = correspondence_concept
    factory_codelet = FactoryCodelet(Mock(), Mock(), bubble_chamber, Mock())
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
    assert isinstance(
        factory_codelet.child_codelets[0], CorrespondenceBuilder
    ) or isinstance(factory_codelet.child_codelets[1], CorrespondenceBuilder)
    assert isinstance(factory_codelet.child_codelets[0], FactoryCodelet) or isinstance(
        factory_codelet.child_codelets[1], FactoryCodelet
    )


def test_engenders_label_builder(bubble_chamber, builder_concept, label_concept):
    bubble_chamber.concepts["actions"].get_active.return_value = builder_concept
    bubble_chamber.concepts["structures"].get_active.return_value = label_concept
    factory_codelet = FactoryCodelet(Mock(), Mock(), bubble_chamber, Mock())
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
    assert isinstance(factory_codelet.child_codelets[0], LabelBuilder) or isinstance(
        factory_codelet.child_codelets[1], LabelBuilder
    )
    assert isinstance(factory_codelet.child_codelets[0], FactoryCodelet) or isinstance(
        factory_codelet.child_codelets[1], FactoryCodelet
    )


def test_engenders_relation_builder(bubble_chamber, builder_concept, relation_concept):
    bubble_chamber.concepts["actions"].get_active.return_value = builder_concept
    bubble_chamber.concepts["structures"].get_active.return_value = relation_concept
    factory_codelet = FactoryCodelet(Mock(), Mock(), bubble_chamber, Mock())
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
    assert isinstance(factory_codelet.child_codelets[0], RelationBuilder) or isinstance(
        factory_codelet.child_codelets[1], RelationBuilder
    )
    assert isinstance(factory_codelet.child_codelets[0], FactoryCodelet) or isinstance(
        factory_codelet.child_codelets[1], FactoryCodelet
    )


def test_engenders_chunk_builder(bubble_chamber, builder_concept, view_concept):
    bubble_chamber.concepts["actions"].get_active.return_value = builder_concept
    bubble_chamber.concepts["structures"].get_active.return_value = view_concept
    factory_codelet = FactoryCodelet(Mock(), Mock(), bubble_chamber, Mock())
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
    assert isinstance(factory_codelet.child_codelets[0], ViewBuilder) or isinstance(
        factory_codelet.child_codelets[1], ViewBuilder
    )
    assert isinstance(factory_codelet.child_codelets[0], FactoryCodelet) or isinstance(
        factory_codelet.child_codelets[1], FactoryCodelet
    )


def test_engenders_chunk_builder(bubble_chamber, builder_concept, word_concept):
    bubble_chamber.concepts["actions"].get_active.return_value = builder_concept
    bubble_chamber.concepts["structures"].get_active.return_value = word_concept
    factory_codelet = FactoryCodelet(Mock(), Mock(), bubble_chamber, Mock())
    factory_codelet.run()
    assert 2 == len(factory_codelet.child_codelets)
    assert isinstance(factory_codelet.child_codelets[0], WordBuilder) or isinstance(
        factory_codelet.child_codelets[1], WordBuilder
    )
    assert isinstance(factory_codelet.child_codelets[0], FactoryCodelet) or isinstance(
        factory_codelet.child_codelets[1], FactoryCodelet
    )
