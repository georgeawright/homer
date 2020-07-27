import statistics
from typing import List, Set, Union

from homer.concept import Concept
from homer.concept_space import ConceptSpace
from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlets.relation import Relation
from homer.perceptlets.textlet import Textlet
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

    def create_label(
        self,
        parent_concept: Concept,
        location: List[Union[float, int]],
        time: Union[float, int],
        strength: float,
    ) -> Label:
        label = Label(parent_concept, location, time, strength)
        self.workspace.add_label(label)
        return label

    def create_group(self, members: List[Perceptlet], strength: float) -> Group:
        value = (
            members[0].value
            if type(members[0].value) == str
            else statistics.fmean(member.value for member in members)
        )
        latitude = statistics.fmean([member.location[0] for member in members])
        longitude = statistics.fmean([member.location[1] for member in members])
        location = [latitude, longitude]
        time = statistics.fmean(member.time for member in members)
        neighbours = set()
        for member in members:
            neighbours |= member.neighbours
        for member in members:
            try:
                neighbours.remove(member)
            except KeyError:
                pass
        group = Group(value, location, time, neighbours, members, strength)
        self.workspace.add_group(group)
        return group

    def create_correspondence(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
    ) -> Correspondence:
        correspondence = Correspondence(
            name, parent_concept, first_argument, second_argument, strength
        )
        self.workspace.add_correspondence(correspondence)
        return correspondence

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

    def create_textlet(
        self,
        text: str,
        constituents: List[Union[Textlet, Word]],
        relations: Set[Relation],
        strength: float,
    ) -> Textlet:
        textlet = Textlet(text, constituents, relations, strength)
        self.workspace.add_textlet(textlet)
        return textlet
