import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import PhraseBuilder
from homer.codelets.suggesters import PhraseSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Phrase
from homer.tools import hasinstance


@pytest.fixture
def s_concept():
    return Mock()


@pytest.fixture
def np_concept():
    return Mock()


@pytest.fixture
def vp_concept():
    return Mock()


@pytest.fixture
def s_np_vp(s_concept, np_concept, vp_concept):
    rule = Mock()
    rule.activation = 1.0
    rule.root = s_concept
    rule.left_branch = np_concept
    rule.right_branch = vp_concept
    return rule


@pytest.fixture
def prep():
    word = Mock()
    word.name = "prep"
    word.unhappiness = 1
    word.members = StructureCollection()
    return word


@pytest.fixture
def noun():
    word = Mock()
    word.name = "noun"
    word.unhappiness = 1
    word.members = StructureCollection()
    return word


@pytest.fixture
def pp_slot(prep, noun):
    phrase = Mock()
    phrase.name = "pp_slot"
    phrase.unhappiness = 1
    phrase.members = StructureCollection({prep, noun})
    return phrase


@pytest.fixture
def bubble_chamber(s_np_vp, pp_slot, prep, noun):
    chamber = Mock()
    chamber.concepts = {"suggest": Mock(), "phrase": Mock()}
    chamber.rules = StructureCollection({s_np_vp})
    chamber.text_fragments = StructureCollection({pp_slot, prep, noun})
    chamber.phrases = StructureCollection()
    pp_slot.potential_rule_mates = StructureCollection({prep, noun})
    prep.potential_rule_mates = StructureCollection({pp_slot, noun})
    noun.potential_rule_mates = StructureCollection({pp_slot, prep})
    return chamber


@pytest.fixture
def s(s_concept):
    phrase = Mock()
    phrase.name = "s"
    phrase.is_slot = False
    phrase.quality = 1
    phrase.parent_concept = s_concept
    return phrase


@pytest.fixture
def s_slot(s_concept):
    phrase = Mock()
    phrase.name = "s_slot"
    phrase.is_slot = True
    phrase.quality = 1
    phrase.parent_concept = s_concept
    return phrase


@pytest.fixture
def np(np_concept):
    phrase = Mock()
    phrase.name = "np"
    phrase.is_slot = False
    phrase.quality = 1
    phrase.location = Location([[0], [1]], Mock())
    phrase.parent_concept = np_concept
    return phrase


@pytest.fixture
def vp(vp_concept):
    phrase = Mock()
    phrase.name = "vp"
    phrase.is_slot = False
    phrase.quality = 1
    phrase.location = Location([[2], [3]], Mock())
    phrase.parent_concept = vp_concept
    return phrase


def test_gets_a_rule_if_necessary(bubble_chamber, s_slot, np, vp):
    target_structures = {
        "target_root": s_slot,
        "target_left_branch": np,
        "target_right_branch": vp,
        "target_rule": None,
    }
    phrase_suggester = PhraseSuggester(
        "",
        "",
        bubble_chamber,
        target_structures,
        1.0,
    )
    phrase_suggester.run()
    assert phrase_suggester.target_rule is not None


def test_suggests_a_branch_slot(bubble_chamber, s, np, s_np_vp):
    target_structures = {
        "target_root": s,
        "target_left_branch": np,
        "target_right_branch": None,
        "target_rule": s_np_vp,
    }
    phrase_suggester = PhraseSuggester(
        "",
        "",
        bubble_chamber,
        target_structures,
        1.0,
    )
    phrase_suggester.run()
    assert CodeletResult.SUCCESS == phrase_suggester.result
    assert len(phrase_suggester.child_codelets) == 1
    assert isinstance(phrase_suggester.child_codelets[0], PhraseBuilder)


def test_fizzles_if_incompatible_with_rule(bubble_chamber, s, np, s_np_vp):
    target_structures = {
        "target_root": s,
        "target_left_branch": None,
        "target_right_branch": np,
        "target_rule": s_np_vp,
    }
    phrase_suggester = PhraseSuggester(
        "",
        "",
        bubble_chamber,
        target_structures,
        1.0,
    )
    phrase_suggester.run()
    assert CodeletResult.FIZZLE == phrase_suggester.result


def test_suggests_filling_in_a_root_slot(bubble_chamber, s_slot, np, vp, s_np_vp):
    target_structures = {
        "target_root": s_slot,
        "target_left_branch": np,
        "target_right_branch": vp,
        "target_rule": s_np_vp,
    }
    phrase_suggester = PhraseSuggester(
        "",
        "",
        bubble_chamber,
        target_structures,
        1.0,
    )
    phrase_suggester.run()
    assert CodeletResult.SUCCESS == phrase_suggester.result
    assert len(phrase_suggester.child_codelets) == 1
    assert isinstance(phrase_suggester.child_codelets[0], PhraseBuilder)


def test_fizzles_if_root_slot_is_incompatible_with_rule(
    bubble_chamber, s_slot, vp, np, s_np_vp
):
    target_structures = {
        "target_root": s_slot,
        "target_left_branch": vp,
        "target_right_branch": np,
        "target_rule": s_np_vp,
    }
    phrase_suggester = PhraseSuggester(
        "",
        "",
        bubble_chamber,
        target_structures,
        1.0,
    )
    phrase_suggester.run()
    assert CodeletResult.FIZZLE == phrase_suggester.result
