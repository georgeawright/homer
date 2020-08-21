from .bubbles.perceptlets import (
    Correspondence,
    Group,
    Label,
    RawPerceptletFieldSequence,
    Relation,
    Textlet,
    Word,
)
from .event_trace import EventTrace
from .perceptlet_collection import PerceptletCollection


class Workspace:
    def __init__(
        self, event_trace: EventTrace, input_sequence: RawPerceptletFieldSequence
    ):
        self.event_trace = event_trace
        self.input_sequence = input_sequence
        self.raw_perceptlets = PerceptletCollection(
            {
                raw_perceptlet
                for field in input_sequence
                for row in field
                for raw_perceptlet in row
            }
        )
        self.labels = PerceptletCollection()
        self.groups = PerceptletCollection()
        self.correspondences = PerceptletCollection()
        self.relations = PerceptletCollection()
        self.words = PerceptletCollection()
        self.textlets = PerceptletCollection()
        self.perceptlets = PerceptletCollection.union(
            self.raw_perceptlets,
            self.labels,
            self.groups,
            self.correspondences,
            self.relations,
            self.words,
            self.textlets,
        )

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
