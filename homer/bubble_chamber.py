import random
import statistics
from typing import List, Union

from .activation_patterns import PerceptletActivationPattern
from .bubbles import Concept, Perceptlet
from .bubbles.perceptlets import (
    Correspondence,
    Group,
    Label,
    Relation,
    Textlet,
    Word,
)
from .concept_space import ConceptSpace
from .errors import MissingPerceptletError
from .event_trace import EventTrace
from .logger import Logger
from .perceptlet_collection import PerceptletCollection
from .template import Template
from .workspace import Workspace
from .worldview import Worldview


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
        satisfaction = statistics.fmean(
            [
                perceptlet.unhappiness.as_scalar() * perceptlet.activation.as_scalar()
                for perceptlet in self.workspace.perceptlets
            ]
        )
        self.logger.log_satisfaction(satisfaction)
        return satisfaction

    def update_activations(self) -> None:
        self.concept_space.update_activations()

    def get_random_groups(self, amount: int) -> List[Group]:
        if len(self.workspace.groups) < amount:
            raise MissingPerceptletError("There are not enough groups in the workspace")
        return random.sample(self.workspace.groups.perceptlets, amount)

    def get_random_correspondence_type(self) -> Concept:
        return random.sample(self.concept_space.correspondence_types, 1)[0]

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
        confidence: float,
        parent_id: str,
    ) -> Label:
        activation = PerceptletActivationPattern(confidence)
        label = Label(parent_concept, location, activation, parent_id)
        self.workspace.add_label(label)
        self.logger.log(label)
        return label

    def create_group(
        self, members: PerceptletCollection, confidence: float, parent_id: str,
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
        neighbours = PerceptletCollection()
        for member in members:
            neighbours = PerceptletCollection.union(neighbours, member.neighbours)
        for member in members:
            try:
                neighbours.remove(member)
            except KeyError:
                pass
        activation = PerceptletActivationPattern(confidence)
        group = Group(value, location, neighbours, members, activation, parent_id)
        self.workspace.add_group(group)
        self.logger.log(group)
        return group

    def create_correspondence(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        confidence: float,
        parent_id: str,
    ) -> Correspondence:
        activation = PerceptletActivationPattern(confidence)
        correspondence = Correspondence(
            name,
            parent_concept,
            first_argument,
            second_argument,
            activation,
            parent_id,
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
        confidence: float,
        parent_id: str,
    ) -> Relation:
        activation = PerceptletActivationPattern(confidence)
        relation = Relation(
            name,
            parent_concept,
            first_argument,
            second_argument,
            activation,
            parent_id,
        )
        self.workspace.add_relation(relation)
        self.logger.log(relation)
        return relation

    def create_word(
        self, text: str, parent_concept: Concept, confidence: float, parent_id: str,
    ) -> Word:
        activation = PerceptletActivationPattern(confidence)
        word = Word(text, parent_concept, activation, parent_id)
        self.workspace.add_word(word)
        self.logger.log(word)
        return word

    def create_textlet(
        self, template: Template, label: Label, confidence: float, parent_id: str,
    ) -> Textlet:
        concept = label.parent_concept
        text, words = template.get_text_and_words(concept)
        activation = PerceptletActivationPattern(confidence)
        textlet = Textlet(text, template, concept, words, None, activation, parent_id,)
        self.workspace.add_textlet(textlet)
        self.logger.log(textlet)
        return textlet
