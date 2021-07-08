import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import PhraseBuilder
from homer.codelets.suggesters import PhraseSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept, Phrase, Rule
from homer.structures.spaces import WorkingSpace
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    phrase_concept = Concept(
        Mock(),
        Mock(),
        "phrase",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(phrase_concept)
    suggest_concept = Concept(
        Mock(),
        Mock(),
        "suggest",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(suggest_concept)
    relation = Relation(Mock(), Mock(), phrase_concept, suggest_concept, None, None, 1)
    phrase_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def s_concept():
    s = Concept("", "", "s", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return s


@pytest.fixture
def np_concept():
    np = Concept("", "", "np", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return np


@pytest.fixture
def vp_concept():
    vp = Concept("", "", "vp", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return vp


@pytest.fixture
def working_space():
    space = WorkingSpace(
        "", "", "", Mock(), Mock(), [], StructureCollection(), 1, [], []
    )
    return space


@pytest.fixture
def target_root(bubble_chamber, s_concept, working_space):
    location = Location([[None]], working_space)
    chunk = Chunk("", "", [location], StructureCollection(), working_space, 1.0)
    label = Label("", "", chunk, s_concept, working_space, 1.0)
    root = Phrase("", "", chunk, label, 1.0)
    bubble_chamber.phrases.add(root)
    working_space.add(root)
    return root


@pytest.fixture
def target_left_branch(bubble_chamber, np_concept, working_space):
    location = Location([[0], [1]], working_space)
    chunk = Chunk("", "", [location], StructureCollection(), working_space, 1.0)
    label = Label("", "", chunk, np_concept, working_space, 1.0)
    branch = Phrase("", "", chunk, label, 1.0)
    bubble_chamber.phrases.add(branch)
    working_space.add(branch)
    return branch


@pytest.fixture
def target_right_branch(bubble_chamber, vp_concept, working_space):
    location = Location([[2]], working_space)
    chunk = Chunk("", "", [location], StructureCollection(), working_space, 1.0)
    label = Label("", "", chunk, vp_concept, working_space, 1.0)
    branch = Phrase("", "", chunk, label, 1.0)
    bubble_chamber.phrases.add(branch)
    working_space.add(branch)
    return branch


@pytest.fixture
def target_rule(bubble_chamber, s_concept, np_concept, vp_concept):
    rule = Rule(
        "", "", "", Mock(), s_concept, np_concept, vp_concept, stable_activation=1
    )
    bubble_chamber.rules.add(rule)
    return rule


@pytest.mark.skip
def test_gives_high_confidence_for_compatible_phrase_and_spawns_follow_up(
    bubble_chamber, target_root, target_left_branch, target_right_branch, target_rule
):
    parent_id = ""
    urgency = 1.0

    suggester = PhraseSuggester.spawn(
        parent_id,
        bubble_chamber,
        {
            "target_root": target_root,
            "target_left_branch": target_left_branch,
            "target_right_branch": target_right_branch,
            "target_rule": target_rule,
        },
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], PhraseBuilder)
