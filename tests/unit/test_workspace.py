from unittest.mock import Mock

from homer.workspace import Workspace
from homer.perceptlet_collection import PerceptletCollection


def test_add_label():
    raw_inp = [[[Mock()]]]
    workspace = Workspace(Mock(), raw_inp)
    assert set() == workspace.labels.perceptlets
    label = Mock()
    workspace.add_label(label)
    assert {label} == workspace.labels.perceptlets
    assert label in workspace.perceptlets


def test_add_group():
    raw_inp = [[[Mock()]]]
    workspace = Workspace(Mock(), raw_inp)
    assert set() == workspace.groups.perceptlets
    group = Mock()
    workspace.add_group(group)
    assert {group} == workspace.groups.perceptlets
    assert group in workspace.perceptlets


def test_add_correspondence():
    raw_inp = [[[Mock()]]]
    workspace = Workspace(Mock(), raw_inp)
    assert set() == workspace.correspondences.perceptlets
    correspondence = Mock()
    workspace.add_correspondence(correspondence)
    assert {correspondence} == workspace.correspondences.perceptlets
    assert correspondence in workspace.perceptlets


def test_add_relation():
    raw_inp = [[[Mock()]]]
    workspace = Workspace(Mock(), raw_inp)
    assert set() == workspace.relations.perceptlets
    relation = Mock()
    workspace.add_relation(relation)
    assert {relation} == workspace.relations.perceptlets
    assert relation in workspace.perceptlets


def test_add_word():
    raw_inp = [[[Mock()]]]
    workspace = Workspace(Mock(), raw_inp)
    assert set() == workspace.words.perceptlets
    word = Mock()
    workspace.add_word(word)
    assert {word} == workspace.words.perceptlets
    assert word in workspace.perceptlets


def test_add_textlet():
    raw_inp = [[[Mock()]]]
    workspace = Workspace(Mock(), raw_inp)
    assert set() == workspace.textlets.perceptlets
    textlet = Mock()
    workspace.add_textlet(textlet)
    assert {textlet} == workspace.textlets.perceptlets
    assert textlet in workspace.perceptlets
