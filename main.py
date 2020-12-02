import math

from homer import BubbleChamber, Coderack, Homer, StructureCollection
from homer.classifiers import (
    DifferenceClassifier,
    DifferentnessClassifier,
    SamenessClassifier,
    ProximityClassifier,
)
from homer.id import ID
from homer.location import Location
from homer.loggers import DjangoLogger
from homer.structures import Chunk, Concept, Lexeme
from homer.structures.chunks import Word
from homer.structures.chunks.slots import TemplateSlot
from homer.structures.links import Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template
from homer.word_form import WordForm


def link_concepts(concept_1, concept_2, activation=0.0):
    relation = Relation(ID.new(Relation), "", concept_1, concept_2, None, None, 1.0)
    relation._activation = activation
    concept_1.links_in.add(relation)
    concept_1.links_out.add(relation)
    concept_2.links_in.add(relation)
    concept_2.links_out.add(relation)
    return relation


problem = [
    [4, 5, 6, 4, 3],
    [10, 10, 7, 4, 4],
    [10, 11, 13, 16, 17],
    [10, 13, 16, 16, 19],
    [13, 20, 22, 19, 21],
    [22, 22, 24, 23, 22],
]

path_to_logs = "logs"
logger = DjangoLogger.setup(path_to_logs)

top_level_conceptual_space = ConceptualSpace(
    "top_level_space", "", "top level", StructureCollection(), None
)
logger.log(top_level_conceptual_space)
top_level_working_space = top_level_conceptual_space.instance
logger.log(top_level_working_space)
bubble_chamber = BubbleChamber(
    StructureCollection({top_level_conceptual_space}),
    StructureCollection({top_level_working_space}),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    StructureCollection(),
    logger,
)
bubble_chamber.lexemes = StructureCollection()

input_concept = Concept.new(
    "input",
    None,
    None,
    top_level_conceptual_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(input_concept)
bubble_chamber.concepts.add(input_concept)
input_space = WorkingSpace(
    "input_space", "", "input", StructureCollection(), 0.0, input_concept
)
logger.log(input_space)
bubble_chamber.working_spaces.add(input_space)
top_level_working_space.child_spaces.add(input_space)

activity_concept = Concept.new(
    "activity",
    None,
    None,
    top_level_conceptual_space,
    None,
    StructureCollection(),
    None,
)
logger.log(activity_concept)
bubble_chamber.concepts.add(activity_concept)
activities_space = ConceptualSpace(
    "activities", "", "activities", StructureCollection(), None
)
logger.log(activities_space)
bubble_chamber.conceptual_spaces.add(activities_space)
build_concept = Concept.new(
    "build",
    None,
    None,
    activities_space,
    None,
    StructureCollection(),
    None,
)
logger.log(build_concept)
build_concept._activation = 1.0
bubble_chamber.concepts.add(build_concept)
evaluate_concept = Concept.new(
    "evaluate",
    None,
    None,
    activities_space,
    None,
    StructureCollection(),
    None,
)
logger.log(evaluate_concept)
bubble_chamber.concepts.add(evaluate_concept)
select_concept = Concept.new(
    "select",
    None,
    None,
    activities_space,
    None,
    StructureCollection(),
    None,
)
logger.log(select_concept)
bubble_chamber.concepts.add(select_concept)

structure_concept = Concept.new(
    "structure",
    None,
    None,
    top_level_conceptual_space,
    None,
    StructureCollection(),
    None,
)
logger.log(structure_concept)
bubble_chamber.concepts.add(structure_concept)
structures_space = ConceptualSpace(
    "structures", "", "structures", StructureCollection(), None
)
logger.log(structures_space)
bubble_chamber.conceptual_spaces.add(structures_space)
chunk_concept = Concept.new(
    "chunk",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(chunk_concept)
bubble_chamber.concepts.add(chunk_concept)
view_concept = Concept.new(
    "view",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(view_concept)
bubble_chamber.concepts.add(view_concept)
word_concept = Concept.new(
    "word",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(word_concept)
bubble_chamber.concepts.add(word_concept)
label_concept = Concept.new(
    "label",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(label_concept)
bubble_chamber.concepts.add(label_concept)
label_concepts_space = ConceptualSpace(
    "label_concept", "", "label concepts", StructureCollection(), label_concept
)
logger.log(label_concepts_space)
bubble_chamber.conceptual_spaces.add(label_concepts_space)
relation_concept = Concept.new(
    "relation",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(relation_concept)
bubble_chamber.concepts.add(relation_concept)
relational_concepts_space = ConceptualSpace(
    "relational_concepts",
    "",
    "relational concepts",
    StructureCollection(),
    relation_concept,
)
logger.log(relational_concepts_space)
bubble_chamber.conceptual_spaces.add(relational_concepts_space)
correspondence_concept = Concept.new(
    "correspondence",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(correspondence_concept)
bubble_chamber.concepts.add(correspondence_concept)
correspondential_concepts_space = ConceptualSpace(
    "correspondential_concepts",
    "",
    "correspondential concepts",
    StructureCollection(),
    correspondence_concept,
)
logger.log(correspondential_concepts_space)
bubble_chamber.conceptual_spaces.add(correspondential_concepts_space)
template_concept = Concept.new(
    "template",
    None,
    None,
    structures_space,
    None,
    StructureCollection(),
    None,
)
logger.log(template_concept)
bubble_chamber.concepts.add(template_concept)
templates_space = ConceptualSpace(
    "templates", "", "templates", StructureCollection(), template_concept
)
logger.log(templates_space)

link_concepts(build_concept, chunk_concept)
link_concepts(build_concept, correspondence_concept)
link_concepts(build_concept, label_concept, activation=1.0)
link_concepts(build_concept, relation_concept)
link_concepts(build_concept, view_concept)
link_concepts(build_concept, word_concept)

link_concepts(evaluate_concept, chunk_concept)
link_concepts(evaluate_concept, correspondence_concept)
link_concepts(evaluate_concept, label_concept)
link_concepts(evaluate_concept, relation_concept)
link_concepts(evaluate_concept, view_concept)

link_concepts(select_concept, chunk_concept)
link_concepts(select_concept, correspondence_concept)
link_concepts(select_concept, label_concept)
link_concepts(select_concept, relation_concept)
link_concepts(select_concept, view_concept)

link_concepts(build_concept, evaluate_concept, activation=1.0)
link_concepts(evaluate_concept, select_concept, activation=1.0)
link_concepts(select_concept, build_concept, activation=1.0)


temperature_concept = Concept.new(
    "temperature",
    None,
    None,
    label_concepts_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(temperature_concept)
bubble_chamber.concepts.add(temperature_concept)
temperature_space = ConceptualSpace(
    "temperature", "", "temperature", StructureCollection(), temperature_concept
)
logger.log(temperature_space)
label_concepts_space.child_spaces.add(temperature_space)
bubble_chamber.conceptual_spaces.add(temperature_space)
temperature_concept.child_spaces.add(temperature_space)
hot = Concept.new(
    "hot",
    [22],
    ProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(hot)
bubble_chamber.concepts.add(hot)
hot_lexeme = Lexeme.new(
    "hot",
    {
        WordForm.HEADWORD: "hot",
        WordForm.COMPARATIVE: "hotter",
        WordForm.SUPERLATIVE: "hottest",
    },
    hot,
)
logger.log(hot_lexeme)
bubble_chamber.lexemes.add(hot_lexeme)
warm = Concept.new(
    "warm",
    [16],
    ProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(warm)
bubble_chamber.concepts.add(warm)
warm_lexeme = Lexeme.new(
    "warm",
    {
        WordForm.HEADWORD: "warm",
        WordForm.COMPARATIVE: "warmer",
        WordForm.SUPERLATIVE: "warmest",
    },
    warm,
)
logger.log(warm_lexeme)
bubble_chamber.lexemes.add(warm_lexeme)
mild = Concept.new(
    "mild",
    [10],
    ProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(mild)
bubble_chamber.concepts.add(mild)
mild_lexeme = Lexeme.new(
    "mild",
    {
        WordForm.HEADWORD: "mild",
        WordForm.COMPARATIVE: "milder",
        WordForm.SUPERLATIVE: "mildest",
    },
    mild,
)
logger.log(mild_lexeme)
bubble_chamber.lexemes.add(mild_lexeme)
cold = Concept.new(
    "cold",
    [4],
    ProximityClassifier(),
    temperature_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(cold)
bubble_chamber.concepts.add(cold)
cold_lexeme = Lexeme.new(
    "cold",
    {
        WordForm.HEADWORD: "cold",
        WordForm.COMPARATIVE: "colder",
        WordForm.SUPERLATIVE: "coldest",
    },
    cold,
)
bubble_chamber.lexemes.add(cold_lexeme)

location_concept = Concept.new(
    "location",
    None,
    None,
    label_concepts_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(location_concept)
bubble_chamber.concepts.add(location_concept)
location_space = ConceptualSpace(
    "location", "", "location", StructureCollection(), location_concept
)
logger.log(location_space)
label_concepts_space.child_spaces.add(location_space)
bubble_chamber.conceptual_spaces.add(location_space)
location_concept.child_spaces.add(location_space)
north = Concept.new(
    "north",
    [0, 2],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(north)
bubble_chamber.concepts.add(north)
north_lexeme = Lexeme.new(
    "north",
    {
        WordForm.HEADWORD: "north",
        WordForm.COMPARATIVE: "further north",
        WordForm.SUPERLATIVE: "furthest north",
    },
    north,
)
logger.log(north_lexeme)
bubble_chamber.lexemes.add(north_lexeme)
south = Concept.new(
    "south",
    [5, 2],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(south)
bubble_chamber.concepts.add(south)
south_lexeme = Lexeme.new(
    "south",
    {
        WordForm.HEADWORD: "south",
        WordForm.COMPARATIVE: "further south",
        WordForm.SUPERLATIVE: "furthest south",
    },
    south,
)
logger.log(south_lexeme)
bubble_chamber.lexemes.add(south_lexeme)
east = Concept.new(
    "east",
    [2.5, 4],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(east)
bubble_chamber.concepts.add(east)
east_lexeme = Lexeme.new(
    "east",
    {
        WordForm.HEADWORD: "east",
        WordForm.COMPARATIVE: "further east",
        WordForm.SUPERLATIVE: "furthest east",
    },
    east,
)
logger.log(east_lexeme)
bubble_chamber.lexemes.add(east_lexeme)
west = Concept.new(
    "west",
    [2.5, 0],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(west)
bubble_chamber.concepts.add(west)
west_lexeme = Lexeme.new(
    "west",
    {
        WordForm.HEADWORD: "west",
        WordForm.COMPARATIVE: "further west",
        WordForm.SUPERLATIVE: "furthest west",
    },
    west,
)
logger.log(west_lexeme)
bubble_chamber.lexemes.add(west_lexeme)
northwest = Concept.new(
    "northwest",
    [0, 0],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(northwest)
bubble_chamber.concepts.add(northwest)
northwest_lexeme = Lexeme.new(
    "northwest",
    {
        WordForm.HEADWORD: "northwest",
        WordForm.COMPARATIVE: "further northwest",
        WordForm.SUPERLATIVE: "furthest northwest",
    },
    northwest,
)
logger.log(northwest_lexeme)
bubble_chamber.lexemes.add(northwest_lexeme)
northeast = Concept.new(
    "northeast",
    [0, 4],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(northeast)
bubble_chamber.concepts.add(northeast)
northeast_lexeme = Lexeme.new(
    "northeast",
    {
        WordForm.HEADWORD: "northeast",
        WordForm.COMPARATIVE: "further northeast",
        WordForm.SUPERLATIVE: "furthest northeast",
    },
    northeast,
)
logger.log(northeast_lexeme)
bubble_chamber.lexemes.add(northeast_lexeme)
southwest = Concept.new(
    "southwest",
    [5, 0],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(southwest)
bubble_chamber.concepts.add(southwest)
southwest_lexeme = Lexeme.new(
    "southwest",
    {
        WordForm.HEADWORD: "southwest",
        WordForm.COMPARATIVE: "further southwest",
        WordForm.SUPERLATIVE: "furthest southwest",
    },
    southwest,
)
logger.log(southwest_lexeme)
bubble_chamber.lexemes.add(southwest_lexeme)
southeast = Concept.new(
    "southeast",
    [5, 4],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(southeast)
bubble_chamber.concepts.add(southeast)
southeast_lexeme = Lexeme.new(
    "southeast",
    {
        WordForm.HEADWORD: "southeast",
        WordForm.COMPARATIVE: "further southeast",
        WordForm.SUPERLATIVE: "furthest southeast",
    },
    southeast,
)
logger.log(southeast_lexeme)
bubble_chamber.lexemes.add(southeast_lexeme)
midlands = Concept.new(
    "midlands",
    [2.5, 2],
    ProximityClassifier(),
    location_space,
    "coordinates",
    StructureCollection(),
    math.dist,
)
logger.log(midlands)
bubble_chamber.concepts.add(midlands)
midlands_lexeme = Lexeme.new(
    "midlands",
    {
        WordForm.HEADWORD: "midlands",
        WordForm.COMPARATIVE: "further inland",
        WordForm.SUPERLATIVE: "furthest inland",
    },
    midlands,
)
logger.log(midlands_lexeme)
bubble_chamber.lexemes.add(midlands_lexeme)

more_less_concept = Concept.new(
    "more-less",
    None,
    None,
    relational_concepts_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(more_less_concept)
bubble_chamber.concepts.add(more_less_concept)
more_less_space = ConceptualSpace(
    "more-less", "", "more-less", StructureCollection(), more_less_concept
)
logger.log(more_less_space)
more_less_concept.child_spaces.add(more_less_space)
relational_concepts_space.child_spaces.add(more_less_space)
bubble_chamber.conceptual_spaces.add(more_less_space)
more = Concept.new(
    "more",
    [4],
    DifferenceClassifier(ProximityClassifier()),
    more_less_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(more)
bubble_chamber.concepts.add(more)
more_lexeme = Lexeme.new(
    "more",
    {
        WordForm.HEADWORD: "more",
        WordForm.COMPARATIVE: "more",
        WordForm.SUPERLATIVE: "most",
    },
    more,
)
logger.log(more_lexeme)
bubble_chamber.lexemes.add(more_lexeme)
less = Concept.new(
    "less",
    [-4],
    DifferenceClassifier(ProximityClassifier()),
    more_less_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(less)
bubble_chamber.concepts.add(less)
less_lexeme = Lexeme.new(
    "less",
    {
        WordForm.HEADWORD: "less",
        WordForm.COMPARATIVE: "less",
        WordForm.SUPERLATIVE: "least",
    },
    less,
)
logger.log(less_lexeme)
bubble_chamber.lexemes.add(less_lexeme)

same_different_concept = Concept.new(
    "same-different",
    None,
    None,
    correspondential_concepts_space,
    "value",
    StructureCollection(),
    math.dist,
)
logger.log(same_different_concept)
bubble_chamber.concepts.add(same_different_concept)
same_different_space = ConceptualSpace(
    "same-different",
    "",
    "same-different",
    StructureCollection(),
    same_different_concept,
)
logger.log(same_different_space)
bubble_chamber.conceptual_spaces.add(same_different_space)
same = Concept.new(
    "same",
    None,
    SamenessClassifier(),
    same_different_space,
    None,
    StructureCollection(),
    math.dist,
)
logger.log(same)
bubble_chamber.concepts.add(same)
different = Concept.new(
    "different",
    None,
    DifferentnessClassifier(),
    same_different_space,
    None,
    StructureCollection(),
    math.dist,
)
logger.log(different)
bubble_chamber.concepts.add(different)

# TEMPLATE 1: the location is temperature
template_1 = Template(
    ID.new(Template),
    "",
    "the [location] is [temperature]",
    StructureCollection(),
    None,
    parent_spaces=StructureCollection({templates_space}),
)
logger.log(template_1)
word_the = Word(
    ID.new(Word),
    "",
    "the",
    Location([0], template_1),
    StructureCollection({template_1}),
    1.0,
)
logger.log(word_the)
slot_location = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    location_concept,
    WordForm.HEADWORD,
    Location([1], template_1),
    StructureCollection({template_1}),
)
logger.log(slot_location)
word_is = Word(
    ID.new(Word),
    "",
    "is",
    Location([2], template_1),
    StructureCollection({template_1}),
    1.0,
)
logger.log(word_is)
slot_temperature = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    temperature_concept,
    WordForm.HEADWORD,
    Location([3], template_1),
    StructureCollection({template_1}),
)
logger.log(slot_temperature)
template_1.contents.add(word_the)
template_1.contents.add(slot_location)
template_1.contents.add(word_is)
template_1.contents.add(slot_temperature)
bubble_chamber.conceptual_spaces.add(template_1)

# TEMPLATE 2: it is temperature in the location
template_2 = Template(
    ID.new(Template),
    "",
    "it is [temperature] in the [location]",
    StructureCollection(),
    None,
    parent_spaces=StructureCollection({templates_space}),
)
logger.log(template_2)
word_it = Word(
    ID.new(Word),
    "",
    "it",
    Location([0], template_2),
    StructureCollection({template_2}),
    1.0,
)
logger.log(word_it)
word_is = Word(
    ID.new(Word),
    "",
    "is",
    Location([1], template_2),
    StructureCollection({template_2}),
    1.0,
)
slot_temperature = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    temperature_concept,
    WordForm.HEADWORD,
    Location([2], template_2),
    StructureCollection({template_2}),
)
word_in = Word(
    ID.new(Word),
    "",
    "in",
    Location([3], template_2),
    StructureCollection({template_2}),
    1.0,
)
word_the = Word(
    ID.new(Word),
    "",
    "the",
    Location([4], template_2),
    StructureCollection({template_2}),
    1.0,
)
slot_location = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    location_concept,
    WordForm.HEADWORD,
    Location([5], template_2),
    StructureCollection({template_2}),
)

template_2.contents.add(word_it)
template_2.contents.add(word_is)
template_2.contents.add(slot_temperature)
template_2.contents.add(word_in)
template_2.contents.add(word_the)
template_2.contents.add(slot_location)
bubble_chamber.conceptual_spaces.add(template_2)

# TEMPLATE 3: it is temperature.comparative in the location
template_3 = Template(
    ID.new(TemplateSlot),
    "",
    "it is [temperature.comparative] in the [location]",
    StructureCollection(),
    None,
    parent_spaces=StructureCollection({templates_space}),
)
logger.log(template_3)
word_it = Word(
    ID.new(Word),
    "",
    "it",
    Location([0], template_3),
    StructureCollection({template_3}),
    1.0,
)
word_is = Word(
    ID.new(Word),
    "",
    "is",
    Location([1], template_3),
    StructureCollection({template_3}),
    1.0,
)
slot_temperature = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    temperature_concept,
    WordForm.COMPARATIVE,
    Location([2], template_3),
    StructureCollection({template_3}),
)
word_in = Word(
    ID.new(Word),
    "",
    "in",
    Location([3], template_3),
    StructureCollection({template_3}),
    1.0,
)
word_the = Word(
    ID.new(Word),
    "",
    "the",
    Location([4], template_3),
    StructureCollection({template_3}),
    1.0,
)
slot_location = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    location_concept,
    WordForm.HEADWORD,
    Location([5], template_3),
    StructureCollection({template_3}),
)

template_3.contents.add(word_it)
template_3.contents.add(word_is)
template_3.contents.add(slot_temperature)
template_3.contents.add(word_in)
template_3.contents.add(word_the)
template_3.contents.add(slot_location)
bubble_chamber.conceptual_spaces.add(template_3)

# TEMPLATE 4: it is temperature.comparative in the location than the location
template_4 = Template(
    ID.new(TemplateSlot),
    "",
    "it is [temperature.comparative] in the [location] than the [location]",
    StructureCollection(),
    None,
    parent_spaces=StructureCollection({templates_space}),
)
logger.log(template_4)
word_it = Word(
    ID.new(Word),
    "",
    "it",
    Location([0], template_4),
    StructureCollection({template_4}),
    1.0,
)
word_is = Word(
    ID.new(Word),
    "",
    "is",
    Location([1], template_4),
    StructureCollection({template_4}),
    1.0,
)
slot_temperature = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    temperature_concept,
    WordForm.COMPARATIVE,
    Location([2], template_4),
    StructureCollection({template_4}),
)
word_in = Word(
    ID.new(Word),
    "",
    "in",
    Location([3], template_4),
    StructureCollection({template_4}),
    1.0,
)
word_the_1 = Word(
    ID.new(Word),
    "",
    "the",
    Location([4], template_4),
    StructureCollection({template_4}),
    1.0,
)
slot_location_1 = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    location_concept,
    WordForm.HEADWORD,
    Location([5], template_4),
    StructureCollection({template_4}),
)
word_than = Word(
    ID.new(Word),
    "",
    "than",
    Location([6], template_4),
    StructureCollection({template_4}),
    1.0,
)
word_the_2 = Word(
    ID.new(Word),
    "",
    "the",
    Location([7], template_4),
    StructureCollection({template_4}),
    1.0,
)
slot_location_2 = TemplateSlot(
    ID.new(TemplateSlot),
    "",
    location_concept,
    WordForm.HEADWORD,
    Location([8], template_4),
    StructureCollection({template_4}),
)
more_relation = Relation(
    ID.new(Relation), "", slot_location_1, slot_location_2, more, temperature_space, 1.0
)

template_4.contents.add(word_it)
template_4.contents.add(word_is)
template_4.contents.add(slot_temperature)
template_4.contents.add(word_in)
template_4.contents.add(word_the_1)
template_4.contents.add(slot_location_1)
template_4.contents.add(word_than)
template_4.contents.add(word_the_2)
template_4.contents.add(slot_location_2)
bubble_chamber.conceptual_spaces.add(template_4)

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

input_chunks = StructureCollection()
parent_spaces = StructureCollection({bubble_chamber.spaces["input"]})
for i, row in enumerate(problem):
    for j, cell in enumerate(row):
        value = [cell]
        location = Location([i, j], bubble_chamber.spaces["input"])
        members = StructureCollection()
        neighbours = StructureCollection()
        quality = 0.0
        chunk = Chunk(
            ID.new(Chunk),
            "",
            value,
            location,
            members,
            neighbours,
            quality,
            parent_spaces,
        )
        logger.log(chunk)
        input_chunks.add(chunk)
        bubble_chamber.chunks.add(chunk)
        input_space.contents.add(chunk)
for chunk in input_chunks:
    i = chunk.location.coordinates[0]
    j = chunk.location.coordinates[1]
    for x, y in relative_neighbour_coordinates:
        if (
            i + x >= 0
            and i + x < len(problem)
            and j + y >= 0
            and j + y < len(problem[0])
        ):
            neighbour_location = Location([i + x, j + y], input_space)
            chunk.neighbours.add(input_chunks.at(neighbour_location).get_random())

coderack = Coderack.setup(bubble_chamber, logger)

homer = Homer(bubble_chamber, coderack, logger)
homer.run()
