import math

from homer.classifiers import StretchyProximityClassifier
from homer.structure_collection import StructureCollection
from homer.structures import Concept
from homer.structures.spaces import ConceptualSpace

top_level_conceptual_space = ConceptualSpace("top level", StructureCollection(), None)

label_concept = Concept.new(
    "label", None, None, top_level_conceptual_space, None, StructureCollection(), None
)
label_concepts_space = ConceptualSpace(
    "label concepts", StructureCollection(), label_concept
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
location_space = ConceptualSpace("location", StructureCollection(), temperature_concept)
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
