from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.perceptlet import Perceptlet
from homer.workspace import Workspace
from homer.worldview import Worldview
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.relation import Relation
from homer.perceptlets.textlet import Textlet
from homer.perceptlets.word import Word


def test_get_raw_perceptlet():
    workspace = Mock()
    raw_perceptlets = set()
    for _ in range(10):
        raw_perceptlet = Mock()
        raw_perceptlet.importance = 0.5
        raw_perceptlets.add(raw_perceptlet)
    workspace.raw_perceptlets = raw_perceptlets
    bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
    raw_perceptlet = bubble_chamber.get_raw_perceptlet()
    assert raw_perceptlet in workspace.raw_perceptlets


def test_get_random_workspace_concept():
    concept_space = Mock()
    concept_space.workspace_concepts = {Mock() for _ in range(10)}
    bubble_chamber = BubbleChamber(concept_space, Mock(), Mock(), Mock())
    concept = bubble_chamber.get_random_workspace_concept()
    assert concept in concept_space.workspace_concepts


def test_get_random_groups():
    workspace = Mock()
    workspace.groups = {Mock() for _ in range(10)}
    bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
    groups = bubble_chamber.get_random_groups(2)
    for group in groups:
        assert group in workspace.groups


def test_promote_to_worldview():
    with patch.object(Worldview, "add_perceptlet", return_value=None) as add_perceptlet:
        worldview = Worldview(Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), worldview)
        perceptlet = Mock()
        bubble_chamber.promote_to_worldview(perceptlet)
    add_perceptlet.assert_called_once_with(perceptlet)


def test_demote_from_worldview():
    with patch.object(
        Worldview, "remove_perceptlet", return_value=None
    ) as remove_perceptlet:
        perceptlet = Mock()
        worldview = Worldview({perceptlet})
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), worldview)
        bubble_chamber.demote_from_worldview(perceptlet)
    remove_perceptlet.assert_called_once_with(perceptlet)


def test_create_label_returns_label():
    with patch.object(Workspace, "add_label", return_value=None) as add_label:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        label = bubble_chamber.create_label(Mock(), Mock(), Mock())
        assert Label == type(label)
    add_label.assert_called_once_with(label)


def test_create_group_returns_group():
    with patch.object(Workspace, "add_group", return_value=None) as add_group:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        perceptlet_1 = Perceptlet("value", [1, 2, 2], set())
        perceptlet_2 = Perceptlet("value", [1, 2, 3], set())
        group = bubble_chamber.create_group([perceptlet_1, perceptlet_2], Mock())
        assert Group == type(group)
    add_group.assert_called_once_with(group)


def test_create_relation_returns_relation():
    with patch.object(Workspace, "add_relation", return_value=None) as add_relation:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        relation = bubble_chamber.create_relation(
            Mock(), Mock(), Mock(), Mock(), Mock()
        )
        assert Relation == type(relation)
    add_relation.assert_called_once_with(relation)


def test_create_word_returns_word():
    with patch.object(Workspace, "add_word", return_value=None) as add_word:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        word = bubble_chamber.create_word(Mock(), Mock(), Mock())
        assert Word == type(word)
    add_word.assert_called_once_with(word)


def test_create_text_returns_textlet():
    with patch.object(Workspace, "add_textlet", return_value=None) as add_text:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        textlet = bubble_chamber.create_textlet(Mock(), Mock(), Mock(), Mock())
        assert Textlet == type(textlet)
    add_text.assert_called_once_with(textlet)
