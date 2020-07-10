from typing import Set

from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.phrase import Phrase
from homer.perceptlets.relation import Relation
from homer.perceptlets.sentence import Sentence
from homer.perceptlets.text import Text
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
        self.phrases = set()
        self.sentences = set()
        self.texts = set()

    def add_label(self, label: Label):
        self.labels.add(label)

    def add_group(self, group: Group):
        self.groups.add(group)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)

    def add_word(self, word: Word):
        self.words.add(word)

    def add_phrase(self, phrase: Phrase):
        self.phrases.add(phrase)

    def add_sentence(self, sentence: Sentence):
        self.sentences.add(sentence)

    def add_text(self, text: Text):
        self.texts.add(text)
