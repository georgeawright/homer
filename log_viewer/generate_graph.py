import json
import os
import sys

import graphviz

open_curly = "{"
close_curly = "}"


def main(run_id, structure_id, time):
    if "View" in structure_id:
        return generate_view_graph(run_id, structure_id, time)


def generate_view_graph(run_id, view_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    # url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    url = lambda structure_id: f"{structure_id}"
    view_graph = graphviz.Digraph("view_graph", filename="view_graph.gv", engine="dot")
    view_graph.attr(rankdir="TB")
    view_graph.attr(URL=url(view_id))
    view = get_structure_json(run_id, view_id, time)
    frame = get_structure_json(run_id, view["parent_frame"], time)
    correspondences = [
        get_structure_json(run_id, correspondence_id, time)
        for correspondence_id in view["members"]
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
    parent_space_ids = {
        node["parent_space"] for node in concepts + chunks + letter_chunks
    }
    parent_spaces = [
        get_structure_json(run_id, parent_space_id, time)
        for parent_space_id in parent_space_ids
    ]
    cluster_number = 1
    frame_cluster_name = "cluster_0"
    with view_graph.subgraph(name=frame_cluster_name) as frame_graph:
        frame_id = frame["structure_id"]
        frame_graph.attr(URL=url(frame_id))
        color = "pink"
        for space in parent_spaces:
            space_id = space["structure_id"]
            if space_id not in (frame["input_space"], frame["output_space"]):
                continue
            cluster_name = f"cluster_{cluster_number}"
            cluster_number += 1
            sub_graph_concepts = {
                node["structure_id"]: node["name"].upper()
                for node in concepts
                if node["parent_space"] == space_id
            }
            sub_graph_chunks = [
                node["structure_id"]
                for node in chunks
                if node["parent_space"] == space_id
            ]
            sub_graph_letter_chunks = {
                node["structure_id"]: node["name"]
                for node in letter_chunks
                if node["parent_space"] == space_id
            }
            sub_graph_labels = [
                link["structure_id"]
                for link in correspondence_args
                if "Label" in link["structure_id"]
                and link["start"]
                in sub_graph_chunks + list(sub_graph_letter_chunks.keys())
            ]
            sub_graph_relations = [
                link["structure_id"]
                for link in correspondence_args
                if "Relation" in link["structure_id"]
                and link["start"]
                in sub_graph_chunks + list(sub_graph_letter_chunks.keys())
                and link["end"]
                in sub_graph_chunks + list(sub_graph_letter_chunks.keys())
            ]
            with frame_graph.subgraph(name=cluster_name) as c:
                c.attr(style="filled", color=color, URL=url(space_id))
                c.node_attr.update(shape="circle", style="filled", color="white")
                for concept in sub_graph_concepts:
                    c.node(concept, label=sub_graph_concepts[concept], URL=url(concept))
                c.node_attr.update(shape="rectangle", style="filled", color="white")
                for chunk in sub_graph_chunks:
                    c.node(chunk, URL=url(chunk))
                for letter_chunk in sub_graph_letter_chunks:
                    c.node(
                        letter_chunk,
                        label=sub_graph_letter_chunks[letter_chunk],
                        URL=url(letter_chunk),
                    )
                c.node_attr.update(shape="ellipse", style="filled", color="white")
                for label in sub_graph_labels:
                    c.node(label, URL=url(label))
                for relation in sub_graph_relations:
                    c.node(relation, URL=url(relation))
                c.attr(label=space["name"])
        frame_graph.attr(label=frame["name"])
    for space in parent_spaces:
        space_id = space["structure_id"]
        if space_id in (frame["input_space"], frame["output_space"]):
            continue
        color = "lightgrey"
        if space["name"] == "input":
            color = "lightblue"
        if "output" in space["name"]:
            color = "lightgreen"
        cluster_name = f"cluster_{cluster_number}"
        cluster_number += 1
        sub_graph_concepts = {
            node["structure_id"]: node["name"].upper()
            for node in concepts
            if node["parent_space"] == space_id
        }
        sub_graph_chunks = [
            node["structure_id"] for node in chunks if node["parent_space"] == space_id
        ]
        sub_graph_letter_chunks = {
            node["structure_id"]: node["name"]
            for node in letter_chunks
            if node["parent_space"] == space_id
        }
        sub_graph_labels = [
            link["structure_id"]
            for link in correspondence_args
            if "Label" in link["structure_id"]
            and link["start"] in sub_graph_chunks + list(sub_graph_letter_chunks.keys())
        ]
        sub_graph_relations = [
            link["structure_id"]
            for link in correspondence_args
            if "Relation" in link["structure_id"]
            and link["start"] in sub_graph_chunks + list(sub_graph_letter_chunks.keys())
            and link["end"] in sub_graph_chunks + list(sub_graph_letter_chunks.keys())
        ]
        with view_graph.subgraph(name=cluster_name) as c:
            c.attr(style="filled", color=color, URL=url(space_id))
            c.node_attr.update(shape="circle", style="filled", color="white")
            for concept in sub_graph_concepts:
                c.node(concept, label=sub_graph_concepts[concept], URL=url(concept))
            c.node_attr.update(shape="rectangle", style="filled", color="white")
            for chunk in sub_graph_chunks:
                c.node(chunk, URL=url(chunk))
            for letter_chunk in sub_graph_letter_chunks:
                c.node(
                    letter_chunk,
                    label=sub_graph_letter_chunks[letter_chunk],
                    URL=url(letter_chunk),
                )
            c.node_attr.update(shape="ellipse", style="filled", color="white")
            for label in sub_graph_labels:
                c.node(label, URL=url(label))
            for relation in sub_graph_relations:
                c.node(relation, URL=url(relation))
            c.attr(label=space["name"])
    for link in correspondence_args:
        if "Label" in link["structure_id"]:
            view_graph.edge(link["structure_id"], link["start"], label="start")
        if "Relation" in link["structure_id"]:
            view_graph.edge(link["structure_id"], link["start"], label="start")
            view_graph.edge(link["structure_id"], link["end"], label="end")
        if "Label" in link["structure_id"] or "Relation" in link["structure_id"]:
            view_graph.edge(
                link["parent_concept"], link["structure_id"], label="parent_concept"
            )
        if "LetterChunk" in link["structure_id"]:
            for letter_chunk in link["right_branch"]:
                view_graph.edge(link["structure_id"], letter_chunk, label="right")
            for letter_chunk in link["left_branch"]:
                view_graph.edge(link["structure_id"], letter_chunk, label="left")
    for correspondence in correspondences:
        view_graph.edge(
            correspondence["start"],
            correspondence["end"],
            label=correspondence["parent_concept"],
        )
    view_graph.render(
        f"logs/{run_id}/structures/structures/{view_id}/{time}", format="svg"
    )
    return view_graph


def get_structure_json(run_id, structure_id, time):
    time = int(time)
    log_directory = f"logs/{run_id}/structures/structures"
    structure_directory = f"{log_directory}/{structure_id}"
    structure_files = os.listdir(structure_directory)
    latest_file = None
    latest_file_time = -1
    for file_name in structure_files:
        file_time = int(file_name.split(".")[0])
        if time >= file_time > latest_file_time and ".json" in file_name:
            latest_file_time = file_time
            latest_file = file_name
    with open(f"{structure_directory}/{latest_file}") as f:
        structure_json = json.load(f)
    return structure_json


if __name__ == "__main__":
    run_id = sys.argv[1]
    structure_id = sys.argv[2]
    time = sys.argv[3]
    main(sys.argv[1], sys.argv[2], sys.argv[3])
