import pytest
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.workspace import Workspace
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.phrase import Phrase
from homer.perceptlets.relation import Relation
from homer.perceptlets.sentence import Sentence
from homer.perceptlets.text import Text
from homer.perceptlets.word import Word


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
        group = bubble_chamber.create_group(Mock(), Mock())
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


def test_create_phrase_returns_phrase():
    with patch.object(Workspace, "add_phrase", return_value=None) as add_phrase:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        phrase = bubble_chamber.create_phrase(Mock(), Mock(), Mock(), Mock())
        assert Phrase == type(phrase)
    add_phrase.assert_called_once_with(phrase)


def test_create_sentence_returns_sentence():
    with patch.object(Workspace, "add_sentence", return_value=None) as add_sentence:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        sentence = bubble_chamber.create_sentence(Mock(), Mock(), Mock(), Mock())
        assert Sentence == type(sentence)
    add_sentence.assert_called_once_with(sentence)


def test_create_text_returns_text():
    with patch.object(Workspace, "add_text", return_value=None) as add_text:
        workspace = Workspace(Mock(), Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock())
        text = bubble_chamber.create_text(Mock(), Mock(), Mock(), Mock())
        assert Text == type(text)
    add_text.assert_called_once_with(text)
