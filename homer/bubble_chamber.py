import random
import statistics
from typing import List, Optional, Set, Union

from homer.concept import Concept
from homer.concept_space import ConceptSpace
from homer.errors import MissingPerceptletError
from homer.event_trace import EventTrace
from homer.logger import Logger
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
        logger: Logger,
    ):
        self.concept_space = concept_space
        self.event_trace = event_trace
        self.workspace = workspace
        self.worldview = worldview
        self.result = None
        self.logger = logger

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
        perceptlet_choice = None
        highest_weight = 0
        for perceptlet in self.workspace.raw_perceptlets:
            weight = perceptlet.importance
            if weight > highest_weight:
                highest_weight = weight
                perceptlet_choice = perceptlet
        if perceptlet_choice is None:
            perceptlet_choice = random.sample(self.workspace.raw_perceptlets, 1)[0]
        return perceptlet_choice

    def get_unhappy_raw_perceptlet(self) -> Optional[RawPerceptlet]:
        perceptlet_choice = None
        unhappiness = 0.5
        for perceptlet in self.workspace.raw_perceptlets:
            if perceptlet.unhappiness > 0.1 and perceptlet.unhappiness < unhappiness:
                perceptlet_choice = perceptlet
                unhappiness = perceptlet.unhappiness
        return perceptlet_choice

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

    def get_random_conceptual_space(self) -> Concept:
        return random.sample(self.concept_space.conceptual_spaces, 1)[0]

    def get_random_workspace_concept(self) -> Concept:
        return random.sample(self.concept_space.workspace_concepts, 1)[0]

    def get_random_workspace_concept_by_depth(self) -> Concept:
        randomness = random.random()
        if randomness > 0.67:
            return random.sample(
                {
                    concept
                    for concept in self.concept_space.workspace_concepts
                    if concept.depth == 2
                },
                1,
            )[0]
        return random.sample(
            {
                concept
                for concept in self.concept_space.workspace_concepts
                if concept.depth == 1
            },
            1,
        )[0]

    def promote_to_worldview(self, perceptlet: Perceptlet) -> None:
        self.worldview.add_perceptlet(perceptlet)

    def demote_from_worldview(self, perceptlet: Perceptlet) -> None:
        self.worldview.remove_perceptlet(perceptlet)

    def create_label(
        self,
        parent_concept: Concept,
        location: List[Union[float, int]],
        strength: float,
        parent_id: str,
    ) -> Label:
        label = Label(parent_concept, location, strength, parent_id)
        self.workspace.add_label(label)
        self.logger.log(label)
        return label

    def create_group(
        self, members: Set[Perceptlet], strength: float, parent_id: str,
    ) -> Group:
        value = (
            list(members)[0].value
            if type(list(members)[0].value) == str
            else [
                statistics.fmean([member.value[i] for member in members])
                for i in range(len(list(members)[0].value))
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
        group = Group(value, location, neighbours, members, strength, parent_id)
        self.workspace.add_group(group)
        self.logger.log(group)
        return group

    def create_correspondence(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
        parent_id: str,
    ) -> Correspondence:
        correspondence = Correspondence(
            name, parent_concept, first_argument, second_argument, strength, parent_id,
        )
        self.workspace.add_correspondence(correspondence)
        self.logger.log(correspondence)
        return correspondence

    def create_relation(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
        parent_id: str,
    ) -> Relation:
        relation = Relation(
            name, parent_concept, first_argument, second_argument, strength, parent_id,
        )
        self.workspace.add_relation(relation)
        self.logger.log(relation)
        return relation

    def create_word(
        self, text: str, parent_concept: Concept, strength: float, parent_id: str,
    ) -> Word:
        word = Word(text, parent_concept, strength, parent_id)
        self.workspace.add_word(word)
        self.logger.log(word)
        return word

    def create_textlet(
        self,
        text: str,
        constituents: List[Union[Textlet, Word]],
        relations: Set[Relation],
        strength: float,
        parent_id: str,
    ) -> Textlet:
        textlet = Textlet(text, constituents, relations, strength, parent_id)
        self.workspace.add_textlet(textlet)
        self.logger.log(textlet)
        return textlet
