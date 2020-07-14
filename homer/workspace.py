from typing import Set

from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.relation import Relation
from homer.perceptlets.textlet import Textlet
from homer.perceptlets.word import Word


class Workspace:
    def __init__(
        self, event_trace: EventTrace, perceptlets: Set[Perceptlet],
    ):
        self.event_trace = event_trace
        self.perceptlets = perceptlets
        self.labels = set()
        self.groups = set()
        self.relations = set()
        self.words = set()
        self.textlets = set()

    def add_label(self, label: Label):
        self.labels.add(label)

    def add_group(self, group: Group):
        self.groups.add(group)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)

    def add_word(self, word: Word):
        self.words.add(word)

    def add_textlet(self, textlet: Textlet):
        self.textlets.add(textlet)
