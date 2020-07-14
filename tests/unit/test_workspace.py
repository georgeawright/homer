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


def test_add_textlet():
    workspace = Workspace(Mock(), Mock())
    assert set() == workspace.textlets
    textlet = Mock()
    workspace.add_textlet(textlet)
    assert {textlet} == workspace.textlets
