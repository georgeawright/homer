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
from homer.structures import Chunk, Concept
from homer.structures.chunks import Word
from homer.structures.links import Correspondence, Label, Relation
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
        Mock(),
    )
    text_concept = Concept(
        Mock(), Mock(), "text", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(text_concept)
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
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        None,
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
    return chamber


@pytest.fixture
def good_correspondence(bubble_chamber):
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    temperature_working_space = WorkingSpace(
        Mock(),
        Mock(),
        "temperature working",
        StructureCollection(),
        0,
        temperature_concept,
    )
    temperature_conceptual_space = ConceptualSpace(
        Mock(), Mock(), "temperature", StructureCollection(), temperature_concept
    )
    warm_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    parent_concept = bubble_chamber.concepts["text"]
    template = Template(
        Mock(), Mock(), "mock template", StructureCollection(), parent_concept
    )
    same_concept = Concept(
        Mock(),
        Mock(),
        "same",
        None,
        SamenessClassifier(),
        temperature_conceptual_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    start = Label(Mock(), Mock(), Mock(), warm_concept, temperature_working_space, 0.7)
    end = Label(Mock(), Mock(), Mock(), warm_concept, template, 1.0)
    parent_space = bubble_chamber.common_parent_space(
        temperature_working_space, template
    )
    quality = 0.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        temperature_working_space,
        template,
        same_concept,
        parent_space,
        temperature_conceptual_space,
        quality,
    )
    return correspondence


@pytest.fixture
def bad_correspondence(bubble_chamber):
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    temperature_working_space = WorkingSpace(
        Mock(),
        Mock(),
        "temperature working",
        StructureCollection(),
        0,
        temperature_concept,
    )
    temperature_conceptual_space = ConceptualSpace(
        Mock(), Mock(), "temperature", StructureCollection(), temperature_concept
    )
    warm_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    parent_concept = bubble_chamber.concepts["text"]
    template = Template(
        Mock(), Mock(), "mock template", StructureCollection(), parent_concept
    )
    same_concept = Concept(
        Mock(),
        Mock(),
        "same",
        None,
        SamenessClassifier(),
        temperature_conceptual_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    start = Label(Mock(), Mock(), Mock(), warm_concept, temperature_working_space, 0.0)
    end = Label(Mock(), Mock(), Mock(), warm_concept, template, 1.0)
    parent_space = bubble_chamber.common_parent_space(
        temperature_working_space, template
    )
    quality = 1.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        temperature_working_space,
        template,
        same_concept,
        parent_space,
        temperature_conceptual_space,
        quality,
    )
    return correspondence


@pytest.mark.skip
def test_increases_quality_of_good_correspondence(bubble_chamber, good_correspondence):
    original_quality = good_correspondence.quality
    parent_id = ""
    urgency = 1.0
    evaluator = CorrespondenceEvaluator.spawn(
        parent_id, bubble_chamber, good_correspondence, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_correspondence.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], CorrespondenceSelector)


@pytest.mark.skip
def test_decreases_quality_of_bad_label(bubble_chamber, bad_correspondence):
    original_quality = bad_correspondence.quality
    parent_id = ""
    urgency = 1.0
    evaluator = CorrespondenceEvaluator.spawn(
        parent_id, bubble_chamber, bad_correspondence, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_correspondence.quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], CorrespondenceSelector)
