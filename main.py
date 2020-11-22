import math

from homer import BubbleChamber, StructureCollection
from homer.classifiers import (
    DifferenceClassifier,
    DifferentnessClassifier,
    SamenessClassifier,
    StretchyProximityClassifier,
)
from homer.location import Location
from homer.structures import Chunk, Concept
from homer.structures.spaces import ConceptualSpace, WorkingSpace

top_level_conceptual_space = ConceptualSpace("top level", StructureCollection(), None)
top_level_working_space = top_level_conceptual_space.instance
bubble_chamber = BubbleChamber(
    top_level_working_space,
    top_level_conceptual_space,
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    None,
)

input_concept = Concept.new(
    "input",
    None,
    None,
    top_level_working_space,
    None,
    StructureCollection(),
    None,
)
bubble_chamber.concepts.add(input_concept)
input_space = WorkingSpace("input", StructureCollection(), 0.0, input_concept)
bubble_chamber.spaces.add(input_space)

activity_concept = Concept.new(
    "activity",
    None,
    None,
    top_level_conceptual_space,
    None,
    StructureCollection(),
    None,
)
activities_space = ConceptualSpace("activities", StructureCollection(), None)
build_concept = Concept.new(
    "build",
    None,
    None,
    activities_space,
    None,
    StructureCollection(),
    None,
)
evaluate_concept = Concept.new(
    "evaluate",
    None,
    None,
    activities_space,
    None,
    StructureCollection(),
    None,
)
select_concept = Concept.new(
    "select",
    None,
    None,
    activities_space,
    None,
    StructureCollection(),
    None,
)

structure_concept = Concept.new(
    "structure",
    None,
    None,
    top_level_conceptual_space,
    None,
    StructureCollection(),
    None,
)
structures_space = ConceptualSpace("structures", StructureCollection(), None)
chunk_concept = Concept.new(
    "chunk",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
view_concept = Concept.new(
    "view",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
word_concept = Concept.new(
    "word",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
label_concept = Concept.new(
    "label",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
label_concepts_space = ConceptualSpace(
    "label concepts", StructureCollection(), label_concept
)
relation_concept = Concept.new(
    "relation",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
relational_concepts_space = ConceptualSpace(
    "relational concepts", StructureCollection(), relation_concept
)
correspondence_concept = Concept.new(
    "correspondence",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
correspondential_concepts_space = ConceptualSpace(
    "correspondential concepts", StructureCollection(), correspondence_concept
)

temperature_concept = Concept.new(
    "temperature",
    None,
    None,
    label_concepts_space,
    "value",
    StructureCollection(),
    math.dist,
)
temperature_space = ConceptualSpace(
    "temperature", StructureCollection(), temperature_concept
)
hot = Concept.new(
    "hot",
    [22],
    StretchyProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
warm = Concept.new(
    "warm",
    [16],
    StretchyProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
mild = Concept.new(
    "mild",
    [10],
    StretchyProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
cold = Concept.new(
    "cold",
    [4],
    StretchyProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)

location_concept = Concept.new(
    "location",
    None,
    None,
    label_concepts_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
location_space = ConceptualSpace("location", StructureCollection(), location_concept)
north = Concept.new(
    "north",
    [0, 2],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
south = Concept.new(
    "south",
    [5, 2],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
east = Concept.new(
    "east",
    [2.5, 4],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
west = Concept.new(
    "west",
    [2.5, 0],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
northwest = Concept.new(
    "northwest",
    [0, 0],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
northeast = Concept.new(
    "northeast",
    [0, 4],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
southwest = Concept.new(
    "southwest",
    [5, 0],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
southeast = Concept.new(
    "southeast",
    [5, 4],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
midlands = Concept.new(
    "midlands",
    [2.5, 2],
    StretchyProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)

more_less_concept = Concept.new(
    "more-less",
    None,
    None,
    relational_concepts_space,
    "value",
    StructureCollection(),
    math.dist,
)
more_less_space = ConceptualSpace("more-less", StructureCollection(), more_less_concept)
more = Concept.new(
    "more",
    [4],
    DifferenceClassifier(StretchyProximityClassifier()),
    more_less_space,
    "value",
    StructureCollection(),
    math.dist,
)
less = Concept.new(
    "less",
    [-4],
    DifferenceClassifier(StretchyProximityClassifier()),
    more_less_space,
    "value",
    StructureCollection(),
    math.dist,
)

same_different_concept = Concept.new(
    "same-different",
    None,
    None,
    correspondential_concepts_space,
    "value",
    StructureCollection(),
    math.dist,
)
same_different_space = ConceptualSpace(
    "same-different", StructureCollection(), same_different_concept
)
same = Concept.new(
    "same",
    None,
    SamenessClassifier(),
    same_different_space,
    None,
    StructureCollection(),
    math.dist,
)
different = Concept.new(
    "different",
    None,
    DifferentnessClassifier(),
    same_different_space,
    None,
    StructureCollection(),
    math.dist,
)

problem = [
    [4, 5, 6, 4, 3],
    [10, 10, 7, 4, 4],
    [10, 11, 13, 16, 17],
    [10, 13, 16, 16, 19],
    [13, 20, 22, 19, 21],
    [22, 22, 24, 23, 22],
]

relative_neighbour_coordinates = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]

parent_spaces = StructureCollection({bubble_chamber.spaces["input"]})
for i, row in enumerate(problem):
    for j, cell in enumerate(row):
        value = [cell]
        location = Location([i, j], bubble_chamber.spaces["input"])
        members = StructureCollection()
        neighbours = StructureCollection()
        quality = 0.0
        chunk = Chunk(value, location, members, neighbours, quality, parent_spaces)
        bubble_chamber.chunks.add(chunk)
