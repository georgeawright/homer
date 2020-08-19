import random
import statistics
from typing import List, Union

from homer.concept import Concept
from homer.concept_space import ConceptSpace
from homer.errors import MissingPerceptletError
from homer.event_trace import EventTrace
from homer.logger import Logger
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlets.relation import Relation
from homer.perceptlets.textlet import Textlet
from homer.perceptlets.word import Word
from homer.perceptlet_collection import PerceptletCollection
from homer.template import Template
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
        strength: float,
        parent_id: str,
    ) -> Label:
        label = Label(parent_concept, location, strength, parent_id)
        self.workspace.add_label(label)
        self.logger.log(label)
        return label

    def create_group(
        self, members: PerceptletCollection, strength: float, parent_id: str,
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
        group = Group(value, location, neighbours, members, strength, parent_id)
        self.workspace.add_group(group)
        self.logger.log(group)
        return group

    def create_extended_group(
        self,
        original_group: Group,
        new_member: Perceptlet,
        strength: float,
        parent_id: str,
    ) -> Group:
        members = PerceptletCollection.union(
            original_group.members, PerceptletCollection({new_member})
        )
        return self.create_group(members, strength, parent_id)

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
        self, template: Template, label: Label, strength: float, parent_id: str,
    ) -> Textlet:
        concept = label.parent_concept
        text, words = template.get_text_and_words(concept)
        textlet = Textlet(text, template, concept, words, None, strength, parent_id,)
        self.workspace.add_textlet(textlet)
        self.logger.log(textlet)
        return textlet
