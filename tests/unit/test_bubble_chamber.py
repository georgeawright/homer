from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.perceptlet import Perceptlet
from homer.workspace import Workspace
from homer.worldview import Worldview
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.relation import Relation
from homer.perceptlets.textlet import Textlet
from homer.perceptlets.word import Word
from homer.perceptlet_collection import PerceptletCollection
from homer.template import Template


def test_get_random_workspace_concept():
    concept_space = Mock()
    concept_space.workspace_concepts = {Mock() for _ in range(10)}
    bubble_chamber = BubbleChamber(concept_space, Mock(), Mock(), Mock(), Mock())
    concept = bubble_chamber.get_random_workspace_concept()
    assert concept in concept_space.workspace_concepts


def test_get_random_groups():
    workspace = Mock()
    workspace.groups = PerceptletCollection({Mock() for _ in range(10)})
    bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
    groups = bubble_chamber.get_random_groups(2)
    for group in groups:
        assert group in workspace.groups


def test_promote_to_worldview():
    with patch.object(Worldview, "add_perceptlet", return_value=None) as add_perceptlet:
        worldview = Worldview(Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), worldview, Mock())
        perceptlet = Mock()
        bubble_chamber.promote_to_worldview(perceptlet)
    add_perceptlet.assert_called_once_with(perceptlet)


def test_demote_from_worldview():
    with patch.object(
        Worldview, "remove_perceptlet", return_value=None
    ) as remove_perceptlet:
        perceptlet = Mock()
        worldview = Worldview({perceptlet})
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), worldview, Mock())
        bubble_chamber.demote_from_worldview(perceptlet)
    remove_perceptlet.assert_called_once_with(perceptlet)


def test_create_label_returns_label():
    with patch.object(Workspace, "add_label", return_value=None) as add_label:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        label = bubble_chamber.create_label(Mock(), Mock(), Mock(), Mock())
        assert Label == type(label)
    add_label.assert_called_once_with(label)


def test_create_group_returns_group():
    with patch.object(Workspace, "add_group", return_value=None) as add_group:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        perceptlet_1 = Perceptlet("value", [1, 2, 2], PerceptletCollection(), Mock())
        perceptlet_2 = Perceptlet("value", [1, 2, 3], PerceptletCollection(), Mock())
        group = bubble_chamber.create_group(
            [perceptlet_1, perceptlet_2], Mock(), Mock()
        )
        assert Group == type(group)
    add_group.assert_called_once_with(group)


def test_create_extended_group_returns_group():
    with patch.object(Workspace, "add_group", return_value=None) as add_group:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        original_group = Group(
            "value",
            [1, 2, 2],
            PerceptletCollection(),
            PerceptletCollection(),
            Mock(),
            Mock(),
        )
        new_member = Perceptlet("value", [1, 2, 3], PerceptletCollection(), Mock())
        group = bubble_chamber.create_extended_group(
            original_group, new_member, Mock(), Mock()
        )
        assert Group == type(group)
    add_group.assert_called_once_with(group)


def test_create_correspondence_returns_correspondence():
    with patch.object(
        Workspace, "add_correspondence", return_value=None
    ) as add_correspondence:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        correspondence = bubble_chamber.create_correspondence(
            Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
        )
        assert Correspondence == type(correspondence)
    add_correspondence.assert_called_once_with(correspondence)


def test_create_relation_returns_relation():
    with patch.object(Workspace, "add_relation", return_value=None) as add_relation:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        relation = bubble_chamber.create_relation(
            Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
        )
        assert Relation == type(relation)
    add_relation.assert_called_once_with(relation)


def test_create_word_returns_word():
    with patch.object(Workspace, "add_word", return_value=None) as add_word:
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        word = bubble_chamber.create_word(Mock(), Mock(), Mock(), Mock())
        assert Word == type(word)
    add_word.assert_called_once_with(word)


def test_create_textlet_returns_textlet():
    with patch.object(
        Workspace, "add_textlet", return_value=None
    ) as add_text, patch.object(
        Template, "get_text_and_words", return_value=(Mock(), Mock())
    ):
        raw_inp = [[[Mock()]]]
        workspace = Workspace(Mock(), raw_inp)
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        template = Template(Mock())
        textlet = bubble_chamber.create_textlet(template, Mock(), Mock(), Mock())
        assert Textlet == type(textlet)
    add_text.assert_called_once_with(textlet)
