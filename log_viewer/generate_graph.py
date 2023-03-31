import json
import os
import sys

open_curly = "{"
close_curly = "}"


def main(run_id, structure_id, time):
    if "View" in structure_id:
        return generate_view_graph(run_id, structure_id, time)


def generate_view_graph(run_id, view_id, time):
    structure_json = get_structure_json(run_id, view_id, time)
    correspondences = [
        get_structure_json(run_id, correspondence_id, time)
        for correspondence_id in structure_json["members"]
    ]
    correspondence_args = [
        get_structure_json(run_id, correspondence["start"], time)
        for correspondence in correspondences
        if correspondence["parent_view"] == view_id
    ] + [
        get_structure_json(run_id, correspondence["end"], time)
        for correspondence in correspondences
        if correspondence["parent_view"] == view_id
    ]
    nodes = (
        [
            get_structure_json(run_id, link["parent_concept"], time)
            for link in correspondence_args
            if "Label" in link["structure_id"] or "Relation" in link["structure_id"]
        ]
        + [
            get_structure_json(run_id, link["start"], time)
            for link in correspondence_args
            if "Label" in link["structure_id"] or "Relation" in link["structure_id"]
        ]
        + [
            get_structure_json(run_id, link["end"], time)
            for link in correspondence_args
            if "Relation" in link["structure_id"]
        ]
    )
    concepts = [node for node in nodes if "Concept" in node["structure_id"]] + [
        node for node in correspondence_args if "Concept" in node["structure_id"]
    ]
    chunks = [
        node
        for node in nodes
        if "Chunk" in node["structure_id"] and "Letter" not in node["structure_id"]
    ] + [
        node
        for node in correspondence_args
        if "Chunk" in node["structure_id"] and "Letter" not in node["structure_id"]
    ]
    letter_chunks = [
        node for node in nodes if "LetterChunk" in node["structure_id"]
    ] + [node for node in correspondence_args if "LetterChunk" in node["structure_id"]]
    parent_spaces = {node["parent_space"] for node in concepts + chunks + letter_chunks}
    sub_graph_strings = []
    cluster_number = 0
    for space in parent_spaces:
        cluster_name = f"cluster_{cluster_number}"
        cluster_number += 1
        concepts_string = " ".join(
            [node["structure_id"] for node in concepts if node["parent_space"] == space]
        )
        concepts_string += ";" if len(concepts_string) > 0 else ""
        chunks_string = " ".join(
            [node["structure_id"] for node in chunks if node["parent_space"] == space]
        )
        chunks_string += ";" if len(chunks_string) > 0 else ""
        letter_chunks_string = " ".join(
            [
                node["structure_id"]
                for node in letter_chunks
                if node["parent_space"] == space
            ]
        )
        letter_chunks_string += ";" if len(letter_chunks_string) > 0 else ""
        subgraph_string = f"""
    subgraph {cluster_name} {open_curly}
	style=filled;
	color=lightgrey;
        node [shape = circle]; {concepts_string}
        node [shape = rectangle]; {chunks_string}
        node [shape = rectangle]; {letter_chunks_string}
	label = "{space}";
    {close_curly}
"""
        sub_graph_strings.append(subgraph_string)
    subgraphs_string = "\n    ".join(sub_graph_strings)
    labels = " ".join(
        {
            link["structure_id"]
            for link in correspondence_args
            if "Label" in link["structure_id"]
        }
    )
    relations = " ".join(
        {
            link["structure_id"]
            for link in correspondence_args
            if "Relation" in link["structure_id"]
        }
    )
    edge_strings = []
    for arg in correspondence_args:
        if "start" in arg:
            edge_strings.append(
                arg["structure_id"] + " -> " + arg["start"] + ' [label="start"];'
            )
        if "end" in arg:
            edge_strings.append(
                arg["structure_id"] + " -> " + arg["end"] + ' [label="end"];'
            )
        if "parent_concept" in arg:
            edge_strings.append(
                arg["structure_id"]
                + " -> "
                + arg["parent_concept"]
                + ' [label="parent_concept"];'
            )
    for correspondence in correspondences:
        edge_strings.append(
            correspondence["start"]
            + " -> "
            + correspondence["end"]
            + ' [label="'
            + correspondence["parent_concept"]
            + '"];'
        )
    edges = "\n    ".join(edge_strings)
    dot_string = f"""
digraph G {open_curly}
    rankdir = TB;
    {subgraphs_string}
    node [shape = ellipse]; {labels};
    node [shape = ellipse]; {relations};
    {edges}
{close_curly}
"""
    print(dot_string)
    return dot_string


def get_structure_json(run_id, structure_id, time):
    time = int(time)
    log_directory = f"logs/{run_id}/structures/structures"
    structure_directory = f"{log_directory}/{structure_id}"
    structure_files = os.listdir(structure_directory)
    latest_file = None
    latest_file_time = -1
    for file_name in structure_files:
        file_time = int(file_name.split(".")[0])
        if time >= file_time > latest_file_time:
            latest_file_time = file_time
            latest_file = file_name
    with open(f"{structure_directory}/{latest_file}") as f:
        structure_json = json.load(f)
    return structure_json


if __name__ == "__main__":
    # run_id = sys.argv[1]
    # structure_id = sys.argv[2]
    # time = sys.argv[3]
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    run_id = "1679938035.8834429"
    structure_id = "View50"
    time = "3000"
    main(run_id, structure_id, time)
