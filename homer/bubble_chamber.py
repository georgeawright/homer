from typing import List

from homer.concept import Concept
from homer.concept_space import ConceptSpace
from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.phrase import Phrase
from homer.perceptlets.relation import Relation
from homer.perceptlets.sentence import Sentence
from homer.perceptlets.text import Text
from homer.perceptlets.word import Word
from homer.workspace import Workspace
from homer.worldview import Worldview


class BubbleChamber:
    def __init__(
        self,
        concept_space: ConceptSpace,
        event_trace: EventTrace,
        workspace: Workspace,
        worldview: Worldview,
    ):
        self.concept_space = concept_space
        self.event_trace = event_trace
        self.workspace = workspace
        self.worldview = worldview
        self.result = None

    @property
    def satisfaction(self) -> float:
        """Calculate and return overall satisfaction with perceptual structures"""
        pass

    def select_target_perceptlet(self) -> Perceptlet:
        """Return a target for a codelet"""
        pass

    def promote_to_worldview(self, perceptlet: Perceptlet) -> None:
        self.worldview.add_perceptlet(perceptlet)

    def demote_from_worldview(self, perceptlet: Perceptlet) -> None:
        self.worldview.remove_perceptlet(perceptlet)

    def create_label(self, parent_concept: Concept, strength: float) -> Label:
        label = Label(parent_concept, strength)
        self.workspace.add_label(label)
        return label

    def create_group(self, members: List[Perceptlet], strength: float) -> Group:
        group = Group(members, strength)
        self.workspace.add_group(group)
        return group

    def create_relation(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
    ) -> Relation:
        relation = Relation(
            name, parent_concept, first_argument, second_argument, strength
        )
        self.workspace.add_relation(relation)
        return relation

    def create_word(self, text: str, parent_concept: Concept, strength: float) -> Word:
        word = Word(text, parent_concept, strength)
        self.workspace.add_word(word)
        return word

    def create_phrase(
        self, text: str, words: List[Word], relations: List[Relation], strength: float
    ) -> Phrase:
        phrase = Phrase(text, words, relations, strength)
        self.workspace.add_phrase(phrase)
        return phrase

    def create_sentence(
        self,
        text: str,
        phrases: List[Phrase],
        relations: List[Relation],
        strength: float,
    ) -> Sentence:
        sentence = Sentence(text, phrases, relations, strength)
        self.workspace.add_sentence(sentence)
        return sentence

    def create_text(
        self,
        text: str,
        sentences: List[Sentence],
        relations: List[Relation],
        strength: float,
    ) -> Text:
        text = Text(text, sentences, relations, strength)
        self.workspace.add_text(text)
        return text
