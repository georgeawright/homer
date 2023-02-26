import json
import os
import re

from matplotlib import pyplot


def generate_plot(log_directory, structures, field, title):
    figure = pyplot.figure()
    ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_title(title)

    for structure in structures:
        structure_directory = f"{log_directory}/structures/structures/{structure}"
        log_files = os.listdir(structure_directory)
        log_files.sort(key=lambda x: int(x.split(".")[0]))

        field_history_x = []
        field_history_y = []

        for log_file in log_files:
            time = int(log_file.split(".")[0])
            field_history_x.append(time)
            file_name = f"{structure_directory}/{log_file}"
            with open(file_name, "r") as f:
                file_data = json.load(f)
                field_history_y.append(file_data[field])
                label = file_data["name"] if "name" in file_data else structure

        print(field_history_x)
        print()
        print(field_history_y)

        (line,) = ax.plot(field_history_x, field_history_y)
        line.set_label(label)
        ax.legend()
        ax.set_xlabel("Codelets Run")
        ax.set_ylabel(field)

    file_name = title.replace(" ", "_")
    pyplot.savefig(f"{log_directory}/{file_name}.png")


concept_file_map = {
    # activities
    "suggest": None,
    "build": None,
    "evaluate": None,
    "select": None,
    "publish": None,
    # structures
    "correspondence": None,
    "chunk": None,
    "label": None,
    "letter-chunk": None,
    "relation": None,
    "view": None,
    # grammar
    "np": None,
    "ap": None,
    "pp-inessive-location": None,
    "pp-inessive-time": None,
    # semantic
    "temperature": None,
    "hot": None,
    "warm": None,
    "mild": None,
    "cool": None,
    "cold": None,
    "north": None,
    "south": None,
    "east": None,
    "west": None,
    "northwest": None,
    "northeast": None,
    "southwest": None,
    "southeast": None,
    "central": None,
    "everywhere": None,
    "more": None,
    "less": None,
    "same": None,
    "different": None,
}

conceptual_space_file_map = {
    "location": None,
    "north-south": None,
    "west-east": None,
    "northwest-southeast": None,
    "northeast-southwest": None,
    "peripheralness": None,
}

frame_file_map = {
    "ap[jj]": None,
    "np[nn]": None,
    "pp[between-times]": None,
    "pp[in-location]": None,
    "pp[from-to-locations]": None,
    "pp[from-wards-locations]": None,
    "s-be": None,
    "s-[in/de]crease": None,
    "s-move": None,
    "s-spread": None,
    "s-expand": None,
}

log_directories = os.listdir("logs/")
log_directories.sort()
log_directory = "logs/" + log_directories[-1]

structures_directory = f"{log_directory}/structures/structures/"
log_files = os.listdir(structures_directory)
for log_file in log_files:
    if re.match(r"Concept[1-9]", log_file):
        file_name = f"{structures_directory}/{log_file}/0.json"
        try:
            with open(file_name, "r") as f:
                file_data = json.load(f)
                if file_data["name"] in concept_file_map:
                    concept_file_map[file_data["name"]] = log_file
        except FileNotFoundError:
            pass
for log_file in log_files:
    if re.match(r"ConceptualSpace[1-9]", log_file):
        file_name = f"{structures_directory}/{log_file}/0.json"
        try:
            with open(file_name, "r") as f:
                file_data = json.load(f)
                if file_data["name"] in conceptual_space_file_map:
                    conceptual_space_file_map[file_data["name"]] = log_file
        except FileNotFoundError:
            pass
for log_file in log_files:
    if re.match(r"Frame[1-9]", log_file):
        file_name = f"{structures_directory}/{log_file}/0.json"
        try:
            with open(file_name, "r") as f:
                file_data = json.load(f)
                if file_data["name"] in frame_file_map:
                    frame_file_map[file_data["name"]] = log_file
        except FileNotFoundError:
            pass

generate_plot(
    log_directory,
    [
        concept_file_map["suggest"],
        concept_file_map["build"],
        concept_file_map["evaluate"],
        concept_file_map["select"],
        concept_file_map["publish"],
    ],
    "activation",
    "Activity Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["correspondence"],
        concept_file_map["chunk"],
        concept_file_map["label"],
        concept_file_map["letter-chunk"],
        concept_file_map["relation"],
        concept_file_map["view"],
    ],
    "activation",
    "Structure Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["temperature"],
        concept_file_map["hot"],
        concept_file_map["warm"],
        concept_file_map["mild"],
        concept_file_map["cool"],
        concept_file_map["cold"],
    ],
    "activation",
    "Temperature Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["more"],
        concept_file_map["less"],
        concept_file_map["same"],
        concept_file_map["different"],
    ],
    "activation",
    "Other Semantic Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["north"],
        concept_file_map["south"],
        concept_file_map["east"],
        concept_file_map["west"],
        concept_file_map["northwest"],
        concept_file_map["northeast"],
        concept_file_map["southwest"],
        concept_file_map["southeast"],
        concept_file_map["central"],
        concept_file_map["everywhere"],
    ],
    "activation",
    "Location Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["np"],
        concept_file_map["ap"],
        concept_file_map["pp-inessive-location"],
        concept_file_map["pp-inessive-time"],
    ],
    "activation",
    "Grammar Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        conceptual_space_file_map["location"],
        conceptual_space_file_map["north-south"],
        conceptual_space_file_map["west-east"],
        conceptual_space_file_map["northwest-southeast"],
        conceptual_space_file_map["northeast-southwest"],
        conceptual_space_file_map["peripheralness"],
    ],
    "activation",
    "Location Spaces Activation Over Time",
)

generate_plot(
    log_directory,
    [
        frame_file_map["s-be"],
        frame_file_map["s-[in/de]crease"],
        frame_file_map["s-move"],
        frame_file_map["s-spread"],
        frame_file_map["s-expand"],
    ],
    "activation",
    "Sentence Frames Activation Over Time",
)

generate_plot(
    log_directory,
    [
        frame_file_map["ap[jj]"],
        frame_file_map["pp[between-times]"],
        frame_file_map["pp[in-location]"],
        frame_file_map["pp[from-to-locations]"],
        frame_file_map["pp[from-wards-locations]"],
    ],
    "activation",
    "Phrase Frames Activation Over Time",
)
