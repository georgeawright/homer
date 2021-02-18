import math
import statistics

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
from homer.structures.chunks import Slot, Word
from homer.structures.chunks.slots import TemplateSlot
from homer.structures.links import Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template
from homer.word_form import WordForm


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
homer = Homer.setup(logger)

top_level_conceptual_space = homer.bubble_chamber.spaces["top level"]
top_level_working_space = top_level_conceptual_space.instance_in_space(
    None, name="top level working"
)

input_concept = homer.def_concept(
    name="input",
    parent_space=top_level_conceptual_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
input_space = homer.def_working_space(
    name="input",
    parent_concept=input_concept,
    locations=[Location([], top_level_working_space)],
)
activity_concept = homer.def_concept(
    name="activity",
    parent_space=top_level_conceptual_space,
)
activities_space = homer.def_conceptual_space(
    name="activities",
    parent_concept=activity_concept,
    locations=[Location([], top_level_conceptual_space)],
)
build_concept = homer.def_concept(
    name="build",
    parent_space=activities_space,
    activation=1.0,
)
evaluate_concept = homer.def_concept(
    name="evaluate",
    parent_space=activities_space,
)
select_concept = homer.def_concept(
    name="select",
    parent_space=activities_space,
)
structure_concept = homer.def_concept(
    name="structure",
    parent_space=top_level_conceptual_space,
)
structures_space = homer.def_conceptual_space(
    name="structures",
    parent_concept=structure_concept,
    locations=[Location([], top_level_conceptual_space)],
)
chunk_concept = homer.def_concept(
    name="chunk",
    parent_space=structures_space,
)
view_concept = homer.def_concept(
    name="view",
    parent_space=structures_space,
)
word_concept = homer.def_concept(
    name="word",
    parent_space=structures_space,
    instance_type=str,
)
label_concept = homer.def_concept(
    name="label",
    parent_space=structures_space,
)
relation_concept = homer.def_concept(
    name="relation",
    parent_space=structures_space,
)
correspondence_concept = homer.def_concept(
    name="correspondence",
    parent_space=structures_space,
)
template_concept = homer.def_concept(
    name="template",
    parent_space=structures_space,
)
text_concept = homer.def_concept(
    name="text",
    parent_space=structures_space,
    instance_type=str,
)
label_concepts_space = homer.def_conceptual_space(
    name="label concepts",
    parent_concept=label_concept,
    locations=[Location([], top_level_conceptual_space)],
)
relational_concepts_space = homer.def_conceptual_space(
    name="relational concepts",
    parent_concept=relation_concept,
    locations=[Location([], top_level_conceptual_space)],
)
correspondential_concepts_space = homer.def_conceptual_space(
    name="correspondential concepts",
    parent_concept=correspondence_concept,
    locations=[Location([], top_level_conceptual_space)],
)
templates_space = homer.def_conceptual_space(
    name="templates",
    parent_concept=template_concept,
    locations=[Location([], top_level_conceptual_space)],
)
text_space = homer.def_conceptual_space(
    name="text",
    parent_concept=text_concept,
    locations=[Location([], top_level_conceptual_space)],
)
homer.def_concept_link(build_concept, chunk_concept)
homer.def_concept_link(build_concept, correspondence_concept)
homer.def_concept_link(build_concept, label_concept, activation=1.0)
homer.def_concept_link(build_concept, relation_concept)
homer.def_concept_link(build_concept, view_concept)
homer.def_concept_link(build_concept, word_concept)
homer.def_concept_link(evaluate_concept, chunk_concept)
homer.def_concept_link(evaluate_concept, correspondence_concept)
homer.def_concept_link(evaluate_concept, label_concept)
homer.def_concept_link(evaluate_concept, relation_concept)
homer.def_concept_link(evaluate_concept, view_concept)
homer.def_concept_link(evaluate_concept, word_concept)
homer.def_concept_link(select_concept, chunk_concept)
homer.def_concept_link(select_concept, correspondence_concept)
homer.def_concept_link(select_concept, label_concept)
homer.def_concept_link(select_concept, relation_concept)
homer.def_concept_link(select_concept, view_concept)
homer.def_concept_link(select_concept, word_concept)
homer.def_concept_link(build_concept, evaluate_concept, activation=1.0)
homer.def_concept_link(evaluate_concept, select_concept, activation=1.0)
homer.def_concept_link(select_concept, build_concept, activation=1.0)

# Domain Specific Knowledge

temperature_concept = homer.def_concept(
    name="temperature",
    parent_space=label_concepts_space,
    relevant_value="value",
    distance_function=math.dist,
)
temperature_space = homer.def_conceptual_space(
    name="temperature",
    parent_concept=temperature_concept,
    locations=[Location([], label_concepts_space)],
    no_of_dimensions=1,
    is_basic_level=True,
)
hot = homer.def_concept(
    name="hot",
    prototype=[22],
    classifier=ProximityClassifier(),
    parent_space=temperature_space,
    relevant_value="value",
    distance_function=math.dist,
)
hot_lexeme = homer.def_lexeme(
    headword="hot",
    forms={
        WordForm.HEADWORD: "hot",
        WordForm.COMPARATIVE: "hotter",
        WordForm.SUPERLATIVE: "hottest",
    },
    parent_concept=hot,
)
warm = homer.def_concept(
    name="warm",
    prototype=[16],
    classifier=ProximityClassifier(),
    parent_space=temperature_space,
    relevant_value="value",
    distance_function=math.dist,
)
warm_lexeme = homer.def_lexeme(
    headword="warm",
    forms={
        WordForm.HEADWORD: "warm",
        WordForm.COMPARATIVE: "warmer",
        WordForm.SUPERLATIVE: "warmest",
    },
    parent_concept=warm,
)
mild = homer.def_concept(
    name="mild",
    prototype=[10],
    classifier=ProximityClassifier(),
    parent_space=temperature_space,
    relevant_value="value",
    distance_function=math.dist,
)
mild_lexeme = homer.def_lexeme(
    headword="mild",
    forms={
        WordForm.HEADWORD: "mild",
        WordForm.COMPARATIVE: "milder",
        WordForm.SUPERLATIVE: "mildest",
    },
    parent_concept=mild,
)
cold = homer.def_concept(
    name="cold",
    prototype=[4],
    classifier=ProximityClassifier(),
    parent_space=temperature_space,
    relevant_value="value",
    distance_function=math.dist,
)
cold_lexeme = homer.def_lexeme(
    headword="cold",
    forms={
        WordForm.HEADWORD: "cold",
        WordForm.COMPARATIVE: "colder",
        WordForm.SUPERLATIVE: "coldest",
    },
    parent_concept=cold,
)
location_concept = homer.def_concept(
    name="location",
    parent_space=label_concepts_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
north_south_space = homer.def_conceptual_space(
    name="north-south",
    parent_concept=location_concept,
    locations=[Location([], label_concepts_space)],
    no_of_dimensions=1,
    super_space_to_coordinate_function_map={
        "location": lambda location: [location.coordinates[0]]
    },
)
west_east_space = homer.def_conceptual_space(
    name="west-east",
    parent_concept=location_concept,
    locations=[Location([], label_concepts_space)],
    no_of_dimensions=1,
    super_space_to_coordinate_function_map={
        "location": lambda location: [location.coordinates[1]]
    },
)
nw_se_space = homer.def_conceptual_space(
    name="nw-se",
    parent_concept=location_concept,
    locations=[Location([], label_concepts_space)],
    no_of_dimensions=1,
    super_space_to_coordinate_function_map={
        "location": lambda location: [statistics.fmean(location.coordinates)]
    },
)
ne_sw_space = homer.def_conceptual_space(
    name="ne-sw",
    parent_concept=location_concept,
    locations=[Location([], label_concepts_space)],
    no_of_dimensions=1,
    super_space_to_coordinate_function_map={
        "location": lambda location: [
            statistics.fmean([location.coordinates[0], 4 - location.coordinates[1]])
        ]
    },
)
location_space = homer.def_conceptual_space(
    name="location",
    parent_concept=location_concept,
    locations=[Location([], label_concepts_space)],
    no_of_dimensions=2,
    dimensions=[north_south_space, west_east_space],
    sub_spaces=[north_south_space, west_east_space, nw_se_space, ne_sw_space],
    is_basic_level=True,
)
north = homer.def_concept(
    name="north",
    prototype=[0, 2],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
north_lexeme = homer.def_lexeme(
    headword="north",
    forms={
        WordForm.HEADWORD: "north",
        WordForm.COMPARATIVE: "further north",
        WordForm.SUPERLATIVE: "furthest north",
    },
    parent_concept=north,
)
south = homer.def_concept(
    name="south",
    prototype=[5, 2],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
south_lexeme = homer.def_lexeme(
    headword="south",
    forms={
        WordForm.HEADWORD: "south",
        WordForm.COMPARATIVE: "further south",
        WordForm.SUPERLATIVE: "furthest south",
    },
    parent_concept=south,
)
east = homer.def_concept(
    name="east",
    prototype=[2.5, 4],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
east_lexeme = homer.def_lexeme(
    headword="east",
    forms={
        WordForm.HEADWORD: "east",
        WordForm.COMPARATIVE: "further east",
        WordForm.SUPERLATIVE: "furthest east",
    },
    parent_concept=east,
)
west = homer.def_concept(
    name="west",
    prototype=[2.5, 0],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
west_lexeme = homer.def_lexeme(
    headword="west",
    forms={
        WordForm.HEADWORD: "west",
        WordForm.COMPARATIVE: "further west",
        WordForm.SUPERLATIVE: "furthest west",
    },
    parent_concept=west,
)
northwest = homer.def_concept(
    name="northwest",
    prototype=[0, 0],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
northwest_lexeme = homer.def_lexeme(
    headword="northwest",
    forms={
        WordForm.HEADWORD: "northwest",
        WordForm.COMPARATIVE: "further northwest",
        WordForm.SUPERLATIVE: "furthest northwest",
    },
    parent_concept=northwest,
)
northeast = homer.def_concept(
    name="northeast",
    prototype=[0, 4],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
northeast_lexeme = homer.def_lexeme(
    headword="northeast",
    forms={
        WordForm.HEADWORD: "northeast",
        WordForm.COMPARATIVE: "further northeast",
        WordForm.SUPERLATIVE: "furthest northeast",
    },
    parent_concept=northeast,
)
southwest = homer.def_concept(
    name="southwest",
    prototype=[5, 0],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
southwest_lexeme = homer.def_lexeme(
    headword="southwest",
    forms={
        WordForm.HEADWORD: "southwest",
        WordForm.COMPARATIVE: "further southwest",
        WordForm.SUPERLATIVE: "furthest southwest",
    },
    parent_concept=southwest,
)
southeast = homer.def_concept(
    name="southeast",
    prototype=[5, 4],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
southeast_lexeme = homer.def_lexeme(
    headword="southeast",
    forms={
        WordForm.HEADWORD: "southeast",
        WordForm.COMPARATIVE: "further southeast",
        WordForm.SUPERLATIVE: "furthest southeast",
    },
    parent_concept=southeast,
)
midlands = homer.def_concept(
    name="midlands",
    prototype=[2.5, 2],
    classifier=ProximityClassifier(),
    parent_space=location_space,
    relevant_value="coordinates",
    distance_function=math.dist,
)
midlands_lexeme = homer.def_lexeme(
    headword="midlands",
    forms={
        WordForm.HEADWORD: "midlands",
        WordForm.COMPARATIVE: "further inland",
        WordForm.SUPERLATIVE: "furthest inland",
    },
    parent_concept=midlands,
)
more_less_concept = homer.def_concept(
    name="more-less",
    parent_space=relational_concepts_space,
    relevant_value="value",
    distance_function=math.dist,
)
more_less_space = homer.def_conceptual_space(
    name="more-less",
    locations=[Location([], relational_concepts_space)],
    parent_concept=more_less_concept,
    is_basic_level=True,
)
more = homer.def_concept(
    name="more",
    prototype=[4],
    classifier=DifferenceClassifier(ProximityClassifier()),
    parent_space=more_less_space,
    relevant_value="value",
    distance_function=math.dist,
)
more_lexeme = homer.def_lexeme(
    headword="more",
    forms={
        WordForm.HEADWORD: "more",
        WordForm.COMPARATIVE: "more",
        WordForm.SUPERLATIVE: "most",
    },
    parent_concept=more,
)
less = homer.def_concept(
    name="less",
    prototype=[-4],
    classifier=DifferenceClassifier(ProximityClassifier()),
    parent_space=more_less_space,
    relevant_value="value",
    distance_function=math.dist,
)
less_lexeme = homer.def_lexeme(
    headword="less",
    forms={
        WordForm.HEADWORD: "less",
        WordForm.COMPARATIVE: "less",
        WordForm.SUPERLATIVE: "least",
    },
    parent_concept=less,
)
same_different_concept = homer.def_concept(
    name="same-different",
    parent_space=correspondential_concepts_space,
    relevant_value="value",
    distance_function=math.dist,
)
same_different_space = homer.def_conceptual_space(
    name="same-different",
    locations=[Location([], correspondential_concepts_space)],
    parent_concept=same_different_concept,
    is_basic_level=True,
)
same = homer.def_concept(
    name="same",
    classifier=SamenessClassifier(),
    parent_space=same_different_space,
    distance_function=math.dist,
)
different = homer.def_concept(
    name="different",
    classifier=DifferentnessClassifier(),
    parent_space=same_different_space,
    distance_function=math.dist,
)
template_1 = homer.def_template(
    name="the [location] is [temperature]",
    contents=[
        homer.def_word("the"),
        homer.def_template_slot(location_concept, form=WordForm.HEADWORD),
        homer.def_word("is"),
        homer.def_template_slot(temperature_concept, form=WordForm.HEADWORD),
    ],
)
homer.def_correspondence(template_1[1], template_1[3])
template_2 = homer.def_template(
    name="it is [temperature] in the [location]",
    contents=[
        homer.def_word("it"),
        homer.def_word("is"),
        homer.def_template_slot(temperature_concept, form=WordForm.HEADWORD),
        homer.def_word("in"),
        homer.def_word("the"),
        homer.def_template_slot(location_concept, form=WordForm.HEADWORD),
    ],
)
homer.def_correspondence(template_2[2], template_2[5])
template_3 = homer.def_template(
    name="it is [temperature.comparative] in the [location]",
    contents=[
        homer.def_word("it"),
        homer.def_word("is"),
        homer.def_template_slot(temperature_concept, form=WordForm.COMPARATIVE),
        homer.def_word("in"),
        homer.def_word("the"),
        homer.def_template_slot(location_concept, form=WordForm.HEADWORD),
    ],
)
homer.def_correspondence(template_3[2], template_3[5])
template_4 = homer.def_template(
    name="it is [temperature.comparative] in the [location] than the [location]",
    contents=[
        homer.def_word("it"),
        homer.def_word("is"),
        homer.def_template_slot(temperature_concept, form=WordForm.COMPARATIVE),
        homer.def_word("in"),
        homer.def_word("the"),
        homer.def_template_slot(location_concept, form=WordForm.HEADWORD),
        homer.def_word("than"),
        homer.def_word("the"),
        homer.def_template_slot(location_concept, form=WordForm.HEADWORD),
    ],
)

input_chunks = StructureCollection()
for i, row in enumerate(problem):
    for j, cell in enumerate(row):
        value = [cell]
        location = Location([i, j], homer.bubble_chamber.spaces["input"])
        members = StructureCollection()
        quality = 0.0
        chunk = Chunk(
            ID.new(Chunk),
            "",
            value,
            [location],
            members,
            input_space,
            quality,
        )
        logger.log(chunk)
        input_chunks.add(chunk)
        homer.bubble_chamber.chunks.add(chunk)
        input_space.contents.add(chunk)

homer.run()
