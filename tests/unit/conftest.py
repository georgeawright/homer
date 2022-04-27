import pytest
from unittest.mock import Mock

from linguoplotter.random_machine import RandomMachine
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Correspondence


@pytest.fixture(scope="module")
def bubble_chamber():
    chamber = Mock()

    chamber.loggers = {"activity": Mock(), "structure": Mock(), "errors": Mock()}

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
    inner_concept = Mock()
    inner_concept.name = "inner"
    outer_concept = Mock()
    outer_concept.name = "outer"
    forward_concept = Mock()
    forward_concept.name = "forward"
    chunk_concept = Mock()
    chunk_concept.name = "chunk"
    letter_chunk_concept = Mock()
    letter_chunk_concept.name = "letter-chunk"
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
    same_concept.structure_type = Correspondence
    same_concept.name = "same"
    more_concept = Mock()
    more_concept.name = "more"
    less_concept = Mock()
    less_concept.name = "less"
    chamber.concepts = chamber.new_structure_collection(
        suggest_concept,
        build_concept,
        evaluate_concept,
        select_concept,
        publish_concept,
        inner_concept,
        outer_concept,
        forward_concept,
        chunk_concept,
        letter_chunk_concept,
        label_concept,
        relation_concept,
        correspondence_concept,
        view_simplex_concept,
        view_monitoring_concept,
        text_concept,
        interpretation_concept,
        same_concept,
        more_concept,
        less_concept,
    )
    for concept in chamber.concepts:
        concept.activation = 0.5

    chamber.chunks = chamber.new_structure_collection()
    chamber.rules = chamber.new_structure_collection()
    chamber.input_nodes = [Mock()]
    input_space = Mock()
    input_space.name = "input"
    views_space = Mock()
    views_space.name = "views"
    chamber.spaces = chamber.new_structure_collection(input_space, views_space)
    chamber.monitoring_views = chamber.new_structure_collection()

    return chamber
