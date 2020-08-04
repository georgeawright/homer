import random
import statistics
from typing import List, Set, Union

from homer.concept import Concept
from homer.concept_space import ConceptSpace
from homer.errors import MissingPerceptletError
from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.perceptlets.raw_perceptlet import RawPerceptlet
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
        return statistics.fmean(
            [
                perceptlet.unhappiness * perceptlet.importance
                for perceptlet in self.workspace.perceptlets
            ]
        )

    def update_activations(self) -> None:
        self.concept_space.update_activations()

    def get_raw_perceptlet(self) -> RawPerceptlet:
        if len(self.workspace.raw_perceptlets) < 1:
            raise MissingPerceptletError(
                "There are no raw perceptlets in the worksapce"
            )
        return random.sample(self.workspace.raw_perceptlets, 1)[0]

    def get_random_correspondence(self) -> Correspondence:
        if len(self.workspace.correspondences) < 1:
            raise MissingPerceptletError(
                "There are no correspondences in the worksapce"
            )
        return random.sample(self.workspace.correspondences, 1)[0]

    def get_random_groups(self, amount: int) -> List[Group]:
        if len(self.workspace.groups) < amount:
            raise MissingPerceptletError("There are not enough groups in the workspace")
        return random.sample(self.workspace.groups, amount)

    def get_random_workspace_concept(self) -> Concept:
        return random.sample(self.concept_space.workspace_concepts, 1)[0]

    def promote_to_worldview(self, perceptlet: Perceptlet) -> None:
        self.worldview.add_perceptlet(perceptlet)

    def demote_from_worldview(self, perceptlet: Perceptlet) -> None:
        self.worldview.remove_perceptlet(perceptlet)

    def create_label(
        self,
        parent_concept: Concept,
        location: List[Union[float, int]],
        strength: float,
    ) -> Label:
        label = Label(parent_concept, location, strength)
        self.workspace.add_label(label)
        return label

    def create_group(self, members: Set[Perceptlet], strength: float) -> Group:
        value = (
            members[0].value
            if type(members[0].value) == str
            else [
                statistics.fmean([member.value[i] for member in members])
                for i in range(len(members[0].value))
            ]
        )
        time = statistics.fmean([member.location[0] for member in members])
        latitude = statistics.fmean([member.location[1] for member in members])
        longitude = statistics.fmean([member.location[2] for member in members])
        location = [time, latitude, longitude]
        neighbours = set()
        for member in members:
            neighbours |= member.neighbours
        for member in members:
            try:
                neighbours.remove(member)
            except KeyError:
                pass
        group = Group(value, location, neighbours, members, strength)
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
