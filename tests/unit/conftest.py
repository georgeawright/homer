import pytest
from unittest.mock import Mock

from homer.random_machine import RandomMachine
from homer.structure_collection import StructureCollection


@pytest.fixture(scope="module")
def bubble_chamber():
    chamber = Mock()
    chamber.satisfaction = 0.5
    chamber.random_machine = RandomMachine(chamber, seed=1)
    chamber.new_structure_collection = lambda *x: StructureCollection(chamber, x)

    chamber.new_chunk = lambda **x: Mock()
    chamber.new_letter_chunk = lambda **x: Mock()
    chamber.new_correspondence = lambda **x: Mock()
    chamber.new_label = lambda **x: Mock()
    chamber.new_relation = lambda **x: Mock()

    suggest_concept = Mock()
    suggest_concept.name = "suggest"
    build_concept = Mock()
    build_concept.name = "build"
    evaluate_concept = Mock()
    evaluate_concept.name = "evaluate"
    select_concept = Mock()
    select_concept.name = "select"
    publish_concept = Mock()
    publish_concept.name = "publish"
    chunk_concept = Mock()
    chunk_concept.name = "chunk"
    word_concept = Mock()
    word_concept.name = "word"
    label_concept = Mock()
    label_concept.name = "label"
    relation_concept = Mock()
    relation_concept.name = "relation"
    correspondence_concept = Mock()
    correspondence_concept.name = "correspondence"
    view_simplex_concept = Mock()
    view_simplex_concept.name = "view-simplex"
    view_monitoring_concept = Mock()
    view_monitoring_concept.name = "view-monitoring"
    text_concept = Mock()
    text_concept.name = "text"
    interpretation_concept = Mock()
    interpretation_concept.name = "interpretation"
    same_concept = Mock()
    same_concept.name = "same"
    chamber.concepts = chamber.new_structure_collection(
        suggest_concept,
        build_concept,
        evaluate_concept,
        select_concept,
        publish_concept,
        chunk_concept,
        word_concept,
        label_concept,
        relation_concept,
        correspondence_concept,
        view_simplex_concept,
        view_monitoring_concept,
        text_concept,
        interpretation_concept,
        same_concept,
    )

    chamber.chunks = chamber.new_structure_collection()
    chamber.input_nodes = [Mock()]
    input_space = Mock()
    input_space.name = "input"
    views_space = Mock()
    views_space.name = "views"
    chamber.spaces = chamber.new_structure_collection(input_space, views_space)
    chamber.monitoring_views = chamber.new_structure_collection()

    return chamber
