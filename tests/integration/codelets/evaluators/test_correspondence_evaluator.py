import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import SamenessClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.selectors import CorrespondenceSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Word
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
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
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(text_concept)
    correspondence_concept = Concept(
        Mock(),
        Mock(),
        "correspondence",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(correspondence_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(
        Mock(), Mock(), correspondence_concept, evaluate_concept, None, None, 1
    )
    correspondence_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    top_level_space = ConceptualSpace(
        "top level",
        Mock(),
        "top level",
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.conceptual_spaces.add(top_level_space)
    chamber.working_spaces.add(
        top_level_space.instance_in_space(None, name="top level working")
    )
    return chamber


@pytest.fixture
def temperature_concept():
    concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    return concept


@pytest.fixture
def temperature_conceptual_space(temperature_concept):
    space = ConceptualSpace(
        "temperature",
        Mock(),
        "temperature",
        temperature_concept,
        [],
        StructureCollection(),
        1,
        [],
        [],
    )
    return space


@pytest.fixture
def input_space():
    space = WorkingSpace(
        "input",
        Mock(),
        "input",
        Mock(),
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def temperature_working_space(temperature_conceptual_space, input_space):
    space = temperature_conceptual_space.instance_in_space(input_space)
    return space


@pytest.fixture
def warm_concept():
    concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    return concept


@pytest.fixture
def template(bubble_chamber):
    parent_concept = bubble_chamber.concepts["text"]
    template = Template(
        Mock(),
        Mock(),
        "mock template",
        parent_concept,
        Mock(),
        [],
        StructureCollection(),
    )
    return template


@pytest.fixture
def same_concept(temperature_conceptual_space):
    concept = Concept(
        Mock(),
        Mock(),
        "same",
        Mock(),
        SamenessClassifier(),
        temperature_conceptual_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    return concept


@pytest.fixture
def good_correspondence(
    bubble_chamber,
    temperature_conceptual_space,
    temperature_working_space,
    warm_concept,
    template,
    same_concept,
):
    start = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([], temperature_working_space)],
        Mock(),
        temperature_working_space,
        Mock(),
    )
    end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([], temperature_working_space)],
        Mock(),
        temperature_working_space,
        Mock(),
    )
    start_label = Label(
        Mock(), Mock(), start, warm_concept, temperature_working_space, 1.0
    )
    start.links_out.add(start_label)
    end_label = Label(Mock(), Mock(), end, warm_concept, temperature_working_space, 1.0)
    end.links_out.add(end_label)
    quality = 0.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        temperature_working_space,
        template,
        [Mock(), Mock()],
        same_concept,
        temperature_conceptual_space,
        Mock(),
        quality,
    )
    return correspondence


@pytest.fixture
def bad_correspondence(
    bubble_chamber,
    temperature_conceptual_space,
    temperature_working_space,
    warm_concept,
    template,
    same_concept,
):
    start = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([], temperature_working_space)],
        Mock(),
        temperature_working_space,
        Mock(),
    )
    end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([], temperature_working_space)],
        Mock(),
        temperature_working_space,
        Mock(),
    )
    start_label = Label(
        Mock(), Mock(), start, warm_concept, temperature_working_space, 1.0
    )
    start.links_out.add(start_label)
    quality = 1.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        temperature_working_space,
        template,
        [Mock(), Mock()],
        same_concept,
        temperature_conceptual_space,
        Mock(),
        quality,
    )
    return correspondence


def test_increases_quality_of_good_correspondence(bubble_chamber, good_correspondence):
    original_quality = good_correspondence.quality
    parent_id = ""
    urgency = 1.0
    evaluator = CorrespondenceEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({good_correspondence}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_correspondence.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], CorrespondenceSelector)


def test_decreases_quality_of_bad_label(bubble_chamber, bad_correspondence):
    original_quality = bad_correspondence.quality
    parent_id = ""
    urgency = 1.0
    evaluator = CorrespondenceEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({bad_correspondence}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_correspondence.quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], CorrespondenceSelector)
