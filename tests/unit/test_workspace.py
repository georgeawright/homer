from unittest.mock import Mock
from homer.workspace import Workspace


def test_add_label():
    workspace = Workspace(Mock(), set())
    assert set() == workspace.labels
    label = Mock()
    workspace.add_label(label)
    assert {label} == workspace.labels
    assert label in workspace.perceptlets


def test_add_group():
    workspace = Workspace(Mock(), set())
    assert set() == workspace.groups
    group = Mock()
    workspace.add_group(group)
    assert {group} == workspace.groups
    assert group in workspace.perceptlets


def test_add_correspondence():
    workspace = Workspace(Mock(), set())
    assert set() == workspace.correspondences
    correspondence = Mock()
    workspace.add_correspondence(correspondence)
    assert {correspondence} == workspace.correspondences
    assert correspondence in workspace.perceptlets


def test_add_relation():
    workspace = Workspace(Mock(), set())
    assert set() == workspace.relations
    relation = Mock()
    workspace.add_relation(relation)
    assert {relation} == workspace.relations
    assert relation in workspace.perceptlets


def test_add_word():
    workspace = Workspace(Mock(), set())
    assert set() == workspace.words
    word = Mock()
    workspace.add_word(word)
    assert {word} == workspace.words
    assert word in workspace.perceptlets


def test_add_textlet():
    workspace = Workspace(Mock(), set())
    assert set() == workspace.textlets
    textlet = Mock()
    workspace.add_textlet(textlet)
    assert {textlet} == workspace.textlets
    assert textlet in workspace.perceptlets
