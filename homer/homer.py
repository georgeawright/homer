import time

from homer.bubble_chamber import BubbleChamber
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.coderack import Coderack
from homer.concept_space import ConceptSpace
from homer.concepts.correspondence_type import CorrespondenceType
from homer.concepts.euclidean_concept import EuclideanConcept
from homer.concepts.euclidean_space import EuclideanSpace
from homer.concepts.perceptlet_types import (
    CorrespondenceConcept,
    CorrespondenceLabelConcept,
    GroupConcept,
    GroupLabelConcept,
    LabelConcept,
    TextletConcept,
)
from homer.errors import NoMoreCodelets
from homer.event_trace import EventTrace
from homer import fuzzy
from homer.hyper_parameters import HyperParameters
from homer.logger import Logger
from homer.problem import Problem
from homer.template import Template
from homer.workspace import Workspace
from homer.worldview import Worldview


class Homer:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        logger: Logger,
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.logger = logger
        self.activation_update_frequency = activation_update_frequency

    @classmethod
    def setup(cls, path_to_logs: str, path_to_problem: str):
        """Set up every component and sub-component from a configuration file"""
        logger = Logger.setup(path_to_logs)
        problem = Problem(path_to_problem)
        event_trace = EventTrace([])
        workspace = Workspace(event_trace, problem.as_raw_perceptlet_field_sequence())
        worldview = Worldview(set())

        temperature_templates = [Template(["it", "will", "be", None])]
        location_templates = [Template(["in", "the", None])]

        textlet_concept = TextletConcept()
        correspondence_label_concept = CorrespondenceLabelConcept()
        correspondence_concept = CorrespondenceConcept()
        correspondence_concept.connections.add(textlet_concept)
        correspondence_concept.connections.add(correspondence_label_concept)
        group_label_concept = GroupLabelConcept()
        group_concept = GroupConcept()
        group_concept.connections.add(correspondence_concept)
        group_concept.connections.add(group_label_concept)
        label_concept = LabelConcept()
        label_concept.connections.add(group_concept)
        perceptlet_types = {
            textlet_concept,
            correspondence_concept,
            correspondence_label_concept,
            group_concept,
            group_label_concept,
            label_concept,
        }
        correspondence_types = {
            CorrespondenceType(
                "sameness",
                lambda same_labels, proximity: fuzzy.AND(same_labels, proximity),
            ),
            CorrespondenceType(
                "oppositeness",
                lambda same_labels, proximity: fuzzy.AND(
                    fuzzy.NOT(same_labels), fuzzy.NOT(proximity)
                ),
            ),
            CorrespondenceType(
                "extremeness",
                lambda same_labels, proximity: fuzzy.AND(
                    same_labels, fuzzy.NOT(proximity)
                ),
            ),
        }
        temperature_space = EuclideanSpace("temperature", 5, 1.5, temperature_templates)
        location_space = EuclideanSpace("location", 5, 1, location_templates)
        spaces = {temperature_space, location_space}
        workspace_concepts = {
            EuclideanConcept("cold", [4], temperature_space, depth=1, boundary=[7]),
            EuclideanConcept("mild", [10], temperature_space, depth=1),
            EuclideanConcept("warm", [16], temperature_space, depth=1),
            EuclideanConcept("hot", [22], temperature_space, depth=1, boundary=[19]),
            EuclideanConcept(
                "north", [0, 2], location_space, depth=2, relevant_value="location"
            ),
            EuclideanConcept(
                "south", [5, 2], location_space, depth=2, relevant_value="location"
            ),
            EuclideanConcept(
                "east", [2.5, 4], location_space, depth=2, relevant_value="location"
            ),
            EuclideanConcept(
                "west", [2.5, 0], location_space, depth=2, relevant_value="location"
            ),
            EuclideanConcept(
                "northwest", [0, 0], location_space, depth=2, relevant_value="location",
            ),
            EuclideanConcept(
                "northeast", [0, 4], location_space, depth=2, relevant_value="location",
            ),
            EuclideanConcept(
                "southwest", [5, 0], location_space, depth=2, relevant_value="location",
            ),
            EuclideanConcept(
                "southeast", [5, 4], location_space, depth=2, relevant_value="location",
            ),
            EuclideanConcept(
                "midlands", [2.5, 2], location_space, depth=2, relevant_value="location"
            ),
        }

        concept_space = ConceptSpace(
            perceptlet_types, correspondence_types, spaces, workspace_concepts, logger,
        )

        bubble_chamber = BubbleChamber(
            concept_space, event_trace, workspace, worldview, logger,
        )
        coderack = Coderack(bubble_chamber, logger)
        codelets = [
            BottomUpRawPerceptletLabeler(
                bubble_chamber,
                concept_space.get_perceptlet_type_by_name("label"),
                bubble_chamber.workspace.raw_perceptlets.get_random(),
                HyperParameters.STARTER_CODELET_URGENCY,
                "",
            )
            for _ in range(HyperParameters.NO_OF_STARTER_CODELETS)
        ]
        for codelet in codelets:
            coderack.add_codelet(codelet)

        return Homer(bubble_chamber, coderack, logger)

    def run(self):
        while self.bubble_chamber.result is None:
            # time.sleep(1)
            self.logger.log(self.coderack)
            if self.coderack.codelets_run % self.activation_update_frequency == 0:
                self.print_status_update()
                self.bubble_chamber.update_activations()
            try:
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                print("no more codelets")
                self.logger.log("no more codelets")
                for group in self.bubble_chamber.workspace.groups:
                    print([textlet.value for textlet in group.textlets])
                break
            except Exception as e:
                raise e
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        label_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "label"
        ).activation_pattern.get_activation_as_scalar()
        group_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "group"
        ).activation_pattern.get_activation_as_scalar()
        group_label_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "group-label"
        ).activation_pattern.get_activation_as_scalar()
        correspondence_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "correspondence"
        ).activation_pattern.get_activation_as_scalar()
        correspondence_label_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "correspondence-label"
        ).activation_pattern.get_activation_as_scalar()
        textlet_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "textlet"
        ).activation_pattern.get_activation_as_scalar()
        print(
            "================================================================================"
        )
        print(
            f"codelets run: {codelets_run}; label: {label_activation}; group: {group_activation}; gr_label: {group_label_activation}; corresp: {correspondence_activation}; co_label: {correspondence_label_activation}; textlet: {textlet_activation}"
        )
        print(
            "================================================================================"
        )
