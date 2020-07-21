import pytest
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
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        label = bubble_chamber.create_label(Mock(), Mock())
        assert Label == type(label)
    add_label.assert_called_once_with(label)


def test_create_group_returns_group():
    with patch.object(Workspace, "add_group", return_value=None) as add_group:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        perceptlet_1 = Perceptlet("value", set())
        perceptlet_2 = Perceptlet("value", set())
        group = bubble_chamber.create_group([perceptlet_1, perceptlet_2], Mock())
        assert Group == type(group)
    add_group.assert_called_once_with(group)


def test_create_relation_returns_relation():
    with patch.object(Workspace, "add_relation", return_value=None) as add_relation:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        relation = bubble_chamber.create_relation(
            Mock(), Mock(), Mock(), Mock(), Mock()
        )
        assert Relation == type(relation)
    add_relation.assert_called_once_with(relation)


def test_create_word_returns_word():
    with patch.object(Workspace, "add_word", return_value=None) as add_word:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        word = bubble_chamber.create_word(Mock(), Mock(), Mock())
        assert Word == type(word)
    add_word.assert_called_once_with(word)


def test_create_text_returns_textlet():
    with patch.object(Workspace, "add_textlet", return_value=None) as add_text:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        textlet = bubble_chamber.create_textlet(Mock(), Mock(), Mock(), Mock())
        assert Textlet == type(textlet)
    add_text.assert_called_once_with(textlet)
