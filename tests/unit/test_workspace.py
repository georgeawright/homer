from unittest.mock import Mock
from homer.workspace import Workspace


def test_add_label():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.labels
    label = Mock()
    workspace.add_label(label)
    assert {label} == workspace.labels


def test_add_group():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.groups
    group = Mock()
    workspace.add_group(group)
    assert {group} == workspace.groups


def test_add_relation():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.relations
    relation = Mock()
    workspace.add_relation(relation)
    assert {relation} == workspace.relations


def test_add_word():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.words
    word = Mock()
    workspace.add_word(word)
    assert {word} == workspace.words


def test_add_phrase():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.phrases
    phrase = Mock()
    workspace.add_phrase(phrase)
    assert {phrase} == workspace.phrases


def test_add_sentence():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.sentences
    sentence = Mock()
    workspace.add_sentence(sentence)
    assert {sentence} == workspace.sentences


def test_add_text():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.texts
    text = Mock()
    workspace.add_text(text)
    assert {text} == workspace.texts
