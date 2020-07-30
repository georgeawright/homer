from typing import Set

from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlets.raw_perceptlet_field_sequence import RawPerceptletFieldSequence
from homer.perceptlets.relation import Relation
from homer.perceptlets.textlet import Textlet
from homer.perceptlets.word import Word


class Workspace:
    def __init__(
        self, event_trace: EventTrace, input_sequence: RawPerceptletFieldSequence
    ):
        self.event_trace = event_trace
        self.input_sequence = input_sequence
        self.perceptlets = {
            raw_perceptlet
            for field in input_sequence
            for row in field
            for raw_perceptlet in row
        }
        self.labels = set()
        self.groups = set()
        self.correspondences = set()
        self.relations = set()
        self.words = set()
        self.textlets = set()

    def add_label(self, label: Label):
        self.labels.add(label)
        self.perceptlets.add(label)

    def add_group(self, group: Group):
        self.groups.add(group)
        self.perceptlets.add(group)

    def add_correspondence(self, correspondence: Correspondence):
        self.correspondences.add(correspondence)
        self.perceptlets.add(correspondence)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
        self.perceptlets.add(relation)

    def add_word(self, word: Word):
        self.words.add(word)
        self.perceptlets.add(word)

    def add_textlet(self, textlet: Textlet):
        self.textlets.add(textlet)
        self.perceptlets.add(textlet)
