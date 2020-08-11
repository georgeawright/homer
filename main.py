import os
import time
import yaml

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.coderack import Coderack
from homer.concepts.correspondence_type import CorrespondenceType
from homer.concepts.euclidean_concept import EuclideanConcept
from homer.concepts.euclidean_space import EuclideanSpace
from homer.concepts.perceptlet_types import (
    CorrespondenceConcept,
    CorrespondenceLabelConcept,
    GroupConcept,
    GroupLabelConcept,
    LabelConcept,
)
from homer.concept_space import ConceptSpace
from homer.event_trace import EventTrace
from homer.homer import Homer
from homer.hyper_parameters import HyperParameters
from homer.logger import Logger
from homer.perceptlets.raw_perceptlet import RawPerceptlet
from homer.perceptlets.raw_perceptlet_field import RawPerceptletField
from homer.perceptlets.raw_perceptlet_field_sequence import RawPerceptletFieldSequence
from homer.workspace import Workspace
from homer.worldview import Worldview

if not os.path.exists("logs"):
    os.makedirs("logs")
now = time.localtime()
logging_directory = (
    "logs/"
    + str(now.tm_year)
    + str(now.tm_mon)
    + str(now.tm_mday)
    + str(now.tm_hour)
    + str(now.tm_min)
    + str(now.tm_sec)
)
os.makedirs(logging_directory)
os.makedirs(logging_directory + "/concepts")

logger = Logger(logging_directory)

path_to_problem_file = "problems/temperature_problem_1.yaml"

with open(path_to_problem_file) as f:
    model_input = yaml.load(f, Loader=yaml.FullLoader)
    print(model_input)

raw_perceptlets = [
    [RawPerceptlet(cell_value, [0, i, j], set()) for j, cell_value in enumerate(row)]
    for i, row in enumerate(model_input)
]

neighbour_relative_coordinates = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]

for i, row in enumerate(raw_perceptlets):
    for j, perceptlet in enumerate(row):
        for x, y in neighbour_relative_coordinates:
            if (
                i + x >= 0
                and i + x < len(raw_perceptlets)
                and j + y >= 0
                and j + y < len(row)
            ):
                perceptlet.neighbours.add(raw_perceptlets[i + x][j + y])

for neighbour in raw_perceptlets[0][0].neighbours:
    print(neighbour.value)

raw_perceptlet_field = RawPerceptletField(raw_perceptlets, 0, set())
raw_perceptlet_field_sequence = RawPerceptletFieldSequence([raw_perceptlet_field])
event_trace = EventTrace([])
workspace = Workspace(event_trace, raw_perceptlet_field_sequence)
worldview = Worldview(set())

correspondence_concept = CorrespondenceConcept()
correspondence_label_concept = CorrespondenceLabelConcept()
group_concept = GroupConcept()
group_concept.connections.add(correspondence_concept)
group_label_concept = GroupLabelConcept()
label_concept = LabelConcept()
label_concept.connections.add(group_concept)
perceptlet_types = {
    correspondence_concept,
    correspondence_label_concept,
    group_concept,
    group_label_concept,
    label_concept,
}
correspondence_types = {
    CorrespondenceType(
        "sameness", lambda same_labels, proximity: fuzzy.AND(same_labels, proximity)
    ),
    CorrespondenceType(
        "oppositeness",
        lambda same_labels, proximity: fuzzy.AND(
            fuzzy.NOT(same_labels), fuzzy.NOT(proximity)
        ),
    ),
    CorrespondenceType(
        "extremeness",
        lambda same_labels, proximity: fuzzy.AND(same_labels, fuzzy.NOT(proximity)),
    ),
}
temperature_space = EuclideanSpace("temperature", 5, 1.5)
location_space = EuclideanSpace("location", 5, 1)
spaces = {temperature_space, location_space}
workspace_concepts = {
    EuclideanConcept("cold", [4], temperature_space, depth=1, boundary=[7]),
    EuclideanConcept("mild", [10], temperature_space, depth=1),
    EuclideanConcept("warm", [16], temperature_space, depth=1),
    EuclideanConcept("hot", [22], temperature_space, depth=1, boundary=[19]),
    EuclideanConcept(
        "north", [1, 2], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "south", [4, 2], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "east", [2.5, 3], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "west", [2.5, 1], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "northwest", [0.5, 0.5], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "northeast", [0.5, 3.5], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "southwest", [0.5, 0.5], location_space, depth=2, relevant_value="location"
    ),
    EuclideanConcept(
        "southeast", [4.5, 3.5], location_space, depth=2, relevant_value="location"
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
coderack.codelets = [
    BottomUpRawPerceptletLabeler(
        bubble_chamber,
        concept_space.get_perceptlet_type_by_name("label"),
        bubble_chamber.get_raw_perceptlet(),
        HyperParameters.STARTER_CODELET_URGENCY,
        "",
    )
    for _ in range(HyperParameters.NO_OF_STARTER_CODELETS)
]

homer = Homer(bubble_chamber, coderack, logger)
homer.run()
