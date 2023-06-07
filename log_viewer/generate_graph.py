import json
import os
import sys

import graphviz

open_curly = "{"
close_curly = "}"


def main(run_id, structure_id, time):
    if "CompoundConcept" in structure_id[0:7]:
        return generate_concept_graph(run_id, structure_id, time)
    if "Concept" in structure_id[0:7]:
        return generate_concept_graph(run_id, structure_id, time)
    if "Correspondence" in structure_id:
        return generate_correspondence_graph(run_id, structure_id, time)
    if "Chunk" in structure_id[0:5]:
        return generate_chunk_graph(run_id, structure_id, time)
    if "Frame" in structure_id:
        return generate_frame_graph(run_id, structure_id, time)
    if "Label" in structure_id:
        return generate_label_graph(run_id, structure_id, time)
    if "LetterChunk" in structure_id:
        return generate_letter_chunk_graph(run_id, structure_id, time)
    if "ConceptualSpace" in structure_id:
        return generate_conceptual_space_graph(run_id, structure_id, time)
    if "ContextualSpace" in structure_id:
        return generate_contextual_space_graph(run_id, structure_id, time)
    if "Relation" in structure_id:
        return generate_relation_graph(run_id, structure_id, time)
    if "View" in structure_id:
        return generate_view_graph(run_id, structure_id, time)


def generate_concept_graph(run_id, concept_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    concept_graph = graphviz.Digraph(
        "concept_graph", filename="concept_graph.gv", engine="dot"
    )
    concept_graph.attr(rankdir="TB")
    concept = get_structure_json(run_id, concept_id, time)
    links = [
        get_structure_json(run_id, link_id, time)
        for link_id in concept["links_out"] + concept["links_in"]
    ]
    labels = [item for item in links if "Label" in item["structure_id"]]
    relations = [item for item in links if "Relation" in item["structure_id"]]
    relative_ids = [
        r["start"] if r["start"] != concept_id else r["end"] for r in relations
    ]
    relatives = [
        get_structure_json(run_id, relative_id, time) for relative_id in relative_ids
    ]
    link_concepts = [
        get_structure_json(run_id, link["parent_concept"], time)
        for link in labels + relations
    ]
    label = concept["name"].upper() if concept["name"] != "" else None
    concept_graph.node(
        concept["structure_id"],
        label=label,
        shape="doublecircle",
        URL=url(concept["structure_id"]),
    )
    for relative in relatives:
        if relative["structure_id"] == concept_id:
            continue
        shape = "rectangle" if "Chunk" in relative["structure_id"] else "circle"
        label = relative["name"] if relative["name"] != "" else None
        label = label.upper() if "Concept" in relative["structure_id"] else label
        concept_graph.node(
            relative["structure_id"],
            label=label,
            shape=shape,
            URL=url(relative["structure_id"]),
        )
    for label in labels:
        link_concept = [
            c for c in link_concepts if c["structure_id"] == label["parent_concept"]
        ][0]
        if link_concept["name"] == "":
            concept_graph.node(label["structure_id"], URL=url(label["structure_id"]))
        else:
            concept_graph.node(
                label["structure_id"],
                label=link_concept["name"].upper(),
                URL=url(label["structure_id"]),
            )
    for relation in relations:
        link_concept = [
            c for c in link_concepts if c["structure_id"] == relation["parent_concept"]
        ][0]
        if link_concept["name"] == "":
            concept_graph.node(
                relation["structure_id"], URL=url(relation["structure_id"])
            )
        else:
            concept_graph.node(
                relation["structure_id"],
                label=link_concept["name"].upper(),
                URL=url(relation["structure_id"]),
            )
    for label in labels:
        concept_graph.edge(label["structure_id"], label["start"], label="start")
    for relation in relations:
        concept_graph.edge(relation["structure_id"], relation["start"], label="start")
        concept_graph.edge(relation["structure_id"], relation["end"], label="end")
    concept_graph.render(
        f"logs/{run_id}/structures/structures/{concept_id}/{time}", format="svg"
    )
    return concept_graph


def generate_correspondence_graph(run_id, correspondence_id, time):
    def graph_arg(graph, arg):
        if "Chunk" in arg["structure_id"][0:5]:
            graph.node(
                arg["structure_id"], shape="rectangle", URL=url(arg["structure_id"])
            )
        elif "LetterChunk" in arg["structure_id"]:
            graph.node(
                arg["structure_id"],
                label=arg["name"],
                shape="rectangle",
                URL=url(arg["structure_id"]),
            )
        elif "Label" in arg["structure_id"]:
            concept = get_structure_json(run_id, arg["parent_concept"], time)
            graph.node(arg["structure_id"], URL=url(arg["structure_id"]))
            graph.node(
                arg["structure_id"],
                label=concept["name"].upper()
                if concept["name"] != ""
                else concept["structure_id"],
                URL=url(arg["structure_id"]),
            )
            arg_start = get_structure_json(run_id, arg["start"], time)
            arg_start_label = (
                arg_start["name"] if "LetterChunk" in arg["start"] else None
            )
            graph.node(
                arg["start"],
                label=arg_start_label,
                shape="rectangle",
                URL=url(arg["start"]),
            )
            graph.edge(arg["structure_id"], arg["start"], label="start")
        elif "Relation" in arg["structure_id"]:
            concept = get_structure_json(run_id, arg["parent_concept"], time)
            space = get_structure_json(run_id, arg["conceptual_space"], time)
            concept_name = (
                concept["name"].upper()
                if concept["name"] != ""
                else concept["structure_id"]
            )
            space_name = (
                space["name"].upper() if space["name"] != "" else space["structure_id"]
            )
            graph.node(
                arg["structure_id"],
                label=f"{concept_name}-{space_name}",
                URL=url(arg["structure_id"]),
            )
            arg_start = get_structure_json(run_id, arg["start"], time)
            arg_start_label = (
                arg_start["name"] if "LetterChunk" in arg["start"] else None
            )
            graph.node(
                arg["start"],
                label=arg_start_label,
                shape="rectangle",
                URL=url(arg["start"]),
            )
            graph.edge(arg["structure_id"], arg["start"], label="start")
            arg_end = get_structure_json(run_id, arg["end"], time)
            arg_end_label = arg_end["name"] if "LetterChunk" in arg["end"] else None
            graph.node(
                arg["end"], label=arg_end_label, shape="rectangle", URL=url(arg["end"])
            )
            graph.edge(arg["structure_id"], arg["end"], label="end")

    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    correspondence_graph = graphviz.Digraph(
        "correspondence_graph", filename="correspondence_graph.gv", engine="dot"
    )
    correspondence_graph.attr(rankdir="TB")
    correspondence = get_structure_json(run_id, correspondence_id, time)
    start = get_structure_json(run_id, correspondence["start"], time)
    graph_arg(correspondence_graph, start)
    end = get_structure_json(run_id, correspondence["end"], time)
    graph_arg(correspondence_graph, end)
    concept = get_structure_json(run_id, correspondence["parent_concept"], time)
    color = "black" if concept["name"] == "same" else "red"
    correspondence_graph.edge(
        correspondence["start"],
        correspondence["end"],
        style="dashed",
        color=color,
    )
    correspondence_graph.render(
        f"logs/{run_id}/structures/structures/{correspondence_id}/{time}", format="svg"
    )
    return correspondence_graph


def generate_chunk_graph(run_id, chunk_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    chunk_graph = graphviz.Digraph(
        "chunk_graph", filename="chunk_graph.gv", engine="dot"
    )
    chunk_graph.attr(rankdir="TB")
    chunk = get_structure_json(run_id, chunk_id, time)
    links = [
        get_structure_json(run_id, link_id, time)
        for link_id in chunk["links_out"] + chunk["links_in"]
    ]
    labels = [item for item in links if "Label" in item["structure_id"]]
    relations = [item for item in links if "Relation" in item["structure_id"]]
    relative_ids = [
        r["start"] if r["start"] != chunk_id else r["end"] for r in relations
    ]
    concepts = [
        get_structure_json(run_id, link["parent_concept"], time)
        for link in labels + relations
    ]
    conceptual_spaces = [
        get_structure_json(run_id, relation["conceptual_space"], time)
        for relation in relations
    ]
    chunk_graph.node(
        chunk["structure_id"], shape="doublecircle", URL=url(chunk["structure_id"])
    )
    for relative_id in relative_ids + chunk["members"]:
        if relative_id == chunk_id:
            continue
        chunk_graph.node(relative_id, shape="rectangle", URL=url(relative_id))
    for label in labels:
        concept = [c for c in concepts if c["structure_id"] == label["parent_concept"]][
            0
        ]
        if concept["name"] == "":
            chunk_graph.node(label["structure_id"], URL=url(label["structure_id"]))
        else:
            chunk_graph.node(
                label["structure_id"],
                label=concept["name"].upper(),
                URL=url(label["structure_id"]),
            )
    for relation in relations:
        concept = [
            c for c in concepts if c["structure_id"] == relation["parent_concept"]
        ][0]
        space = [
            s
            for s in conceptual_spaces
            if s["structure_id"] == relation["conceptual_space"]
        ][0]
        concept_name = (
            concept["name"].upper()
            if concept["name"] != ""
            else concept["structure_id"]
        )
        space_name = (
            space["name"].upper() if space["name"] != "" else space["structure_id"]
        )
        link_label = f"{concept_name}-{space_name}"
        chunk_graph.node(
            relation["structure_id"],
            label=link_label,
            URL=url(relation["structure_id"]),
        )
    for label in labels:
        chunk_graph.edge(label["structure_id"], label["start"], label="start")
    for relation in relations:
        chunk_graph.edge(relation["structure_id"], relation["start"], label="start")
        chunk_graph.edge(relation["structure_id"], relation["end"], label="end")
    for member in chunk["members"]:
        chunk_graph.edge(chunk["structure_id"], member, label="member")
    chunk_graph.render(
        f"logs/{run_id}/structures/structures/{chunk_id}/{time}", format="svg"
    )
    return chunk_graph


def generate_frame_graph(run_id, frame_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    frame_graph = graphviz.Digraph(
        "frame_graph", filename="frame_graph.gv", engine="dot"
    )
    frame_graph.attr(rankdir="TB")
    frame_graph.attr(URL=url(frame_id))
    frame = get_structure_json(run_id, frame_id, time)
    spaces = [
        get_structure_json(run_id, space_id, time)
        for space_id in [frame["input_space"], frame["output_space"]]
    ]
    color = "pink"
    cluster_number = 0
    for space in spaces:
        space_id = space["structure_id"]
        if space_id not in (frame["input_space"], frame["output_space"]):
            continue
        cluster_name = f"cluster_{cluster_number}"
        cluster_number += 1
        contents = [
            get_structure_json(run_id, item_id, time) for item_id in space["contents"]
        ]
        chunks = [item for item in contents if "Chunk" in item["structure_id"][0:5]]
        letter_chunks = [
            item for item in contents if "LetterChunk" in item["structure_id"]
        ]
        labels = [item for item in contents if "Label" in item["structure_id"]]
        relations = [item for item in contents if "Relation" in item["structure_id"]]
        link_concepts = [
            get_structure_json(run_id, link["parent_concept"], time)
            for link in labels + relations
        ]
        conceptual_spaces = [
            get_structure_json(run_id, link["conceptual_space"], time)
            for link in relations
            if link["conceptual_space"] is not None
        ] + [{"structure_id": None, "name": ""}]
        with frame_graph.subgraph(name=cluster_name) as c:
            c.attr(style="filled", color=color, URL=url(space_id))
            c.node_attr.update(shape="rectangle", style="filled", color="white")
            for chunk in chunks:
                c.node(chunk["structure_id"], URL=url(chunk["structure_id"]))
            for letter_chunk in letter_chunks:
                label = letter_chunk["name"] if letter_chunk["name"] != "" else None
                c.node(
                    letter_chunk["structure_id"],
                    label=label,
                    URL=url(letter_chunk["structure_id"]),
                )
            c.node_attr.update(shape="ellipse", style="filled", color="white")
            for label in labels:
                link_concept = [
                    c
                    for c in link_concepts
                    if c["structure_id"] == label["parent_concept"]
                ][0]
                link_label = (
                    link_concept["name"].upper() if link_concept["name"] != "" else None
                )
                c.node(
                    label["structure_id"],
                    label=link_label,
                    URL=url(label["structure_id"]),
                )
            for relation in relations:
                link_concept = [
                    c
                    for c in link_concepts
                    if c["structure_id"] == relation["parent_concept"]
                ][0]
                link_space = [
                    s
                    for s in conceptual_spaces
                    if s["structure_id"] == relation["conceptual_space"]
                ][0]
                concept_name = (
                    link_concept["name"].upper()
                    if link_concept["name"] != ""
                    else link_concept["structure_id"]
                )
                space_name = (
                    link_space["name"].upper()
                    if link_space["name"] != ""
                    else link_space["structure_id"]
                )
                link_label = f"{concept_name}-{space_name}"
                c.node(
                    relation["structure_id"],
                    label=link_label,
                    URL=url(relation["structure_id"]),
                )
            for label in labels:
                c.edge(label["structure_id"], label["start"], label="start")
            for relation in relations:
                print(relation)
                c.edge(relation["structure_id"], relation["start"], label="start")
                c.edge(relation["structure_id"], relation["end"], label="end")
            for chunk in chunks:
                for member in chunk["members"]:
                    c.edge(chunk["structure_id"], member, label="member")
            for letter_chunk in letter_chunks:
                for child in letter_chunk["right_branch"]:
                    c.edge(letter_chunk["structure_id"], child, label="right")
                for child in letter_chunk["left_branch"]:
                    c.edge(letter_chunk["structure_id"], child, label="left")
            c.attr(label=space["name"])
    frame_graph.attr(label=frame["name"])
    frame_graph.render(
        f"logs/{run_id}/structures/structures/{frame_id}/{time}", format="svg"
    )
    return frame_graph


def generate_label_graph(run_id, label_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    label_graph = graphviz.Digraph(
        "label_graph", filename="label_graph.gv", engine="dot"
    )
    label_graph.attr(rankdir="TB")
    label = get_structure_json(run_id, label_id, time)
    concept = get_structure_json(run_id, label["parent_concept"], time)
    label_graph.node(
        label["structure_id"],
        label=concept["name"].upper()
        if concept["name"] != ""
        else concept["structure_id"],
        URL=url(label["structure_id"]),
    )
    label_graph.node(label["start"], shape="rectangle", URL=url(label["start"]))
    label_graph.edge(label["structure_id"], label["start"], label="start")
    label_graph.render(
        f"logs/{run_id}/structures/structures/{label_id}/{time}", format="svg"
    )
    return label_graph


def generate_letter_chunk_graph(run_id, letter_chunk_id, time):
    def graph_child(graph, node):
        graph.node(
            node["structure_id"],
            label=node["name"],
            shape="rectangle",
            URL=url(node["structure_id"]),
        )
        for child in node["left_branch"]:
            graph_child(graph, get_structure_json(run_id, child, time))
            graph.edge(node["structure_id"], child, label="left")
        for child in node["right_branch"]:
            graph_child(graph, get_structure_json(run_id, child, time))
            graph.edge(node["structure_id"], child, label="right")

    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    letter_chunk_graph = graphviz.Digraph(
        "letter_chunk_graph", filename="letter_chunk_graph.gv", engine="dot"
    )
    letter_chunk_graph.attr(rankdir="TB")
    letter_chunk = get_structure_json(run_id, letter_chunk_id, time)
    graph_child(letter_chunk_graph, letter_chunk)
    links = [
        get_structure_json(run_id, link_id, time)
        for link_id in letter_chunk["links_out"] + letter_chunk["links_in"]
    ]
    labels = [item for item in links if "Label" in item["structure_id"]]
    relations = [item for item in links if "Relation" in item["structure_id"]]
    relative_ids = [
        r["start"] if r["start"] != letter_chunk["structure_id"] else r["end"]
        for r in relations
    ]
    relatives = [
        get_structure_json(run_id, relative_id, time) for relative_id in relative_ids
    ]
    concepts = [
        get_structure_json(run_id, link["parent_concept"], time)
        for link in labels + relations
    ]
    for relative in relatives:
        if relative["structure_id"] == letter_chunk_id:
            continue
        shape = "rectangle" if "Chunk" in relative["structure_id"] else "circle"
        label = relative["name"] if relative["name"] != "" else None
        label = label.upper() if "Concept" in relative["structure_id"] else label
        letter_chunk_graph.node(
            relative["structure_id"],
            label=label,
            shape=shape,
            URL=url(relative["structure_id"]),
        )

    for label in labels:
        concept = [c for c in concepts if c["structure_id"] == label["parent_concept"]][
            0
        ]
        if concept["name"] == "":
            letter_chunk_graph.node(
                label["structure_id"], URL=url(label["structure_id"])
            )
        else:
            letter_chunk_graph.node(
                label["structure_id"],
                label=concept["name"].upper(),
                URL=url(label["structure_id"]),
            )
    for relation in relations:
        concept = [
            c for c in concepts if c["structure_id"] == relation["parent_concept"]
        ][0]
        if concept["name"] == "":
            letter_chunk_graph.node(
                relation["structure_id"], URL=url(relation["structure_id"])
            )
        else:
            letter_chunk_graph.node(
                relation["structure_id"],
                label=concept["name"].upper(),
                URL=url(relation["structure_id"]),
            )
    for label in labels:
        letter_chunk_graph.edge(label["structure_id"], label["start"], label="start")
    for relation in relations:
        letter_chunk_graph.edge(
            relation["structure_id"], relation["start"], label="start"
        )
        letter_chunk_graph.edge(relation["structure_id"], relation["end"], label="end")
    letter_chunk_graph.render(
        f"logs/{run_id}/structures/structures/{letter_chunk_id}/{time}", format="svg"
    )
    return letter_chunk_graph


def generate_conceptual_space_graph(run_id, space_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    space_graph = graphviz.Digraph(
        "space_graph", filename="space_graph.gv", engine="dot"
    )
    space_graph.attr(rankdir="TB")
    space_graph.attr(style="filled", color="lightgrey", URL=url(space_id))
    space = get_structure_json(run_id, space_id, time)
    contents = [
        get_structure_json(run_id, structure_id, time)
        for structure_id in space["contents"]
    ]
    concepts = [
        item
        for item in contents
        if "Concept" in item["structure_id"] and item["name"] is not None
    ]
    for concept in concepts:
        if concept["name"] == "":
            continue
        space_graph.node(
            concept["structure_id"],
            label=concept["name"].upper(),
            shape="circle",
            URL=url(concept["structure_id"]),
        )
    space_graph.render(
        f"logs/{run_id}/structures/structures/{space_id}/{time}", format="svg"
    )
    return space_graph


def generate_contextual_space_graph(run_id, space_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    space_graph = graphviz.Digraph(
        "space_graph", filename="space_graph.gv", engine="dot"
    )
    space_graph.attr(rankdir="TB")
    space_graph.attr(style="filled", color="lightgrey", URL=url(space_id))
    space = get_structure_json(run_id, space_id, time)
    contents = [
        get_structure_json(run_id, structure_id, time)
        for structure_id in space["contents"]
    ]
    chunks = [
        item
        for item in contents
        if "Chunk" in item["structure_id"] and "Letter" not in item["structure_id"]
    ]
    letter_chunks = [item for item in contents if "LetterChunk" in item["structure_id"]]
    labels = [
        item
        for item in contents
        if "Label" in item["structure_id"]
        and (not space["is_main_input"] or item["activation"] == 1)
    ]
    relations = [
        item
        for item in contents
        if "Relation" in item["structure_id"]
        and (not space["is_main_input"] or item["activation"] == 1)
    ]
    concepts = [
        get_structure_json(run_id, link["parent_concept"], time)
        for link in labels + relations
    ]
    conceptual_spaces = [
        get_structure_json(run_id, relation["conceptual_space"], time)
        for relation in relations
    ]
    for chunk in chunks:
        space_graph.node(
            chunk["structure_id"], shape="rectangle", URL=url(chunk["structure_id"])
        )
    for letter_chunk in letter_chunks:
        space_graph.node(
            letter_chunk["structure_id"],
            label=letter_chunk["name"],
            URL=url(letter_chunk["structure_id"]),
            shape="rectangle",
        )
    space_graph.node_attr.update(shape="ellipse", style="filled", color="lightgrey")
    for label in labels:
        link_concept = [
            c for c in concepts if c["structure_id"] == label["parent_concept"]
        ][0]
        link_label = (
            link_concept["name"].upper()
            if link_concept["name"] != ""
            else link_concept["structure_id"]
        )
        space_graph.node(
            label["structure_id"],
            label=link_label,
            URL=url(label["structure_id"]),
        )
    for relation in relations:
        link_concept = [
            c for c in concepts if c["structure_id"] == relation["parent_concept"]
        ][0]
        link_space = [
            s
            for s in conceptual_spaces
            if s["structure_id"] == relation["conceptual_space"]
        ][0]
        concept_name = (
            link_concept["name"].upper()
            if link_concept["name"] != ""
            else link_concept["structure_id"]
        )
        space_name = (
            link_space["name"].upper()
            if link_space["name"] != ""
            else link_space["structure_id"]
        )
        link_label = f"{concept_name}-{space_name}"
        space_graph.node(
            relation["structure_id"],
            label=link_label,
            URL=url(relation["structure_id"]),
        )
    for label in labels:
        space_graph.edge(label["structure_id"], label["start"], label="start")
    for relation in relations:
        space_graph.edge(relation["structure_id"], relation["start"], label="start")
        space_graph.edge(relation["structure_id"], relation["end"], label="end")
    for letter_chunk in letter_chunks:
        for child in letter_chunk["right_branch"]:
            space_graph.edge(letter_chunk["structure_id"], child, label="right")
        for child in letter_chunk["left_branch"]:
            space_graph.edge(letter_chunk["structure_id"], child, label="left")
    for chunk in chunks:
        for member in chunk["members"]:
            space_graph.edge(chunk["structure_id"], member, label="member")
    space_graph.render(
        f"logs/{run_id}/structures/structures/{space_id}/{time}", format="svg"
    )
    return space_graph


def generate_relation_graph(run_id, relation_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    relation_graph = graphviz.Digraph(
        "relation_graph", filename="relation_graph.gv", engine="dot"
    )
    relation_graph.attr(rankdir="TB")
    relation = get_structure_json(run_id, relation_id, time)
    concept = get_structure_json(run_id, relation["parent_concept"], time)
    space = get_structure_json(run_id, relation["conceptual_space"], time)
    concept_name = (
        concept["name"].upper() if concept["name"] != "" else concept["structure_id"]
    )
    space_name = space["name"].upper() if space["name"] != "" else space["structure_id"]
    relation_graph.node(
        relation["structure_id"],
        label=f"{concept_name}-{space_name}",
        URL=url(relation["structure_id"]),
    )
    relation_graph.node(
        relation["start"], shape="rectangle", URL=url(relation["start"])
    )
    relation_graph.node(relation["end"], shape="rectangle", URL=url(relation["end"]))
    relation_graph.edge(relation["structure_id"], relation["start"], label="start")
    relation_graph.edge(relation["structure_id"], relation["end"], label="end")
    relation_graph.render(
        f"logs/{run_id}/structures/structures/{relation_id}/{time}", format="svg"
    )
    return relation_graph


def generate_view_graph(run_id, view_id, time):
    basic_url = f"structure_snapshot?run_id={run_id}&time={time}"
    url = lambda structure_id: f"{basic_url}&structure_id={structure_id}"
    view_graph = graphviz.Digraph("view_graph", filename="view_graph.gv", engine="dot")
    view_graph.attr(rankdir="TB")
    view_graph.attr(URL=url(view_id))
    view = get_structure_json(run_id, view_id, time)
    frame = get_structure_json(run_id, view["parent_frame"], time)
    correspondences = [
        get_structure_json(run_id, correspondence_id, time)
        for correspondence_id in view["members"]
    ]
    correspondences = [c for c in correspondences if c["parent_view"] == view_id]
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
    labels = [arg for arg in correspondence_args if "Label" in arg["structure_id"]]
    relations = [
        arg for arg in correspondence_args if "Relation" in arg["structure_id"]
    ]
    conceptual_spaces = [
        get_structure_json(run_id, relation["conceptual_space"], time)
        for relation in relations
        if relation["conceptual_space"] is not None
    ] + [{"structure_id": None, "name": ""}]
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
            sub_graph_chunks = [c for c in chunks if c["parent_space"] == space_id]
            sub_graph_letter_chunks = [
                l for l in letter_chunks if l["parent_space"] == space_id
            ]
            sub_graph_labels = [
                l
                for l in labels
                if any(
                    [
                        c["structure_id"] == l["start"]
                        for c in sub_graph_chunks + sub_graph_letter_chunks
                    ]
                )
            ]
            sub_graph_relations = [
                r
                for r in relations
                if any(
                    [
                        c["structure_id"] in (r["start"], r["end"])
                        for c in sub_graph_chunks + sub_graph_letter_chunks
                    ]
                )
            ]
            with frame_graph.subgraph(name=cluster_name) as c:
                c.attr(style="filled", color=color, URL=url(space_id))
                c.node_attr.update(shape="rectangle", style="filled", color="white")
                for chunk in sub_graph_chunks:
                    c.node(chunk["structure_id"], URL=url(chunk["structure_id"]))
                for letter_chunk in sub_graph_letter_chunks:
                    label = letter_chunk["name"] if letter_chunk["name"] != "" else None
                    c.node(
                        letter_chunk["structure_id"],
                        label=label,
                        URL=url(letter_chunk["structure_id"]),
                    )
                c.node_attr.update(shape="ellipse", style="filled", color="white")
                for label in sub_graph_labels:
                    link_concept = [
                        c
                        for c in concepts
                        if c["structure_id"] == label["parent_concept"]
                    ][0]
                    link_label = (
                        link_concept["name"].upper()
                        if link_concept["name"] != ""
                        else link_concept["structure_id"]
                    )
                    c.node(
                        label["structure_id"],
                        label=link_label,
                        URL=url(label["structure_id"]),
                    )
                for relation in sub_graph_relations:
                    link_concept = [
                        c
                        for c in concepts
                        if c["structure_id"] == relation["parent_concept"]
                    ][0]
                    link_space = [
                        s
                        for s in conceptual_spaces
                        if s["structure_id"] == relation["conceptual_space"]
                    ][0]
                    concept_name = (
                        link_concept["name"].upper()
                        if link_concept["name"] != ""
                        else link_concept["structure_id"]
                    )
                    space_name = (
                        link_space["name"].upper()
                        if link_space["name"] != ""
                        else link_space["structure_id"]
                    )
                    link_label = f"{concept_name}-{space_name}"
                    c.node(
                        relation["structure_id"],
                        label=link_label,
                        URL=url(relation["structure_id"]),
                    )
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
        sub_graph_chunks = [c for c in chunks if c["parent_space"] == space_id]
        sub_graph_letter_chunks = [
            l for l in letter_chunks if l["parent_space"] == space_id
        ]
        sub_graph_labels = [
            l
            for l in labels
            if any(
                [
                    c["structure_id"] == l["start"]
                    for c in sub_graph_chunks + sub_graph_letter_chunks
                ]
            )
        ]
        sub_graph_relations = [
            r
            for r in relations
            if any(
                [
                    c["structure_id"] in (r["start"], r["end"])
                    for c in sub_graph_chunks + sub_graph_letter_chunks
                ]
            )
        ]
        with view_graph.subgraph(name=cluster_name) as c:
            c.attr(style="filled", color=color, URL=url(space_id))
            c.node_attr.update(shape="rectangle", style="filled", color="white")
            for chunk in sub_graph_chunks:
                c.node(chunk["structure_id"], URL=url(chunk["structure_id"]))
            for letter_chunk in sub_graph_letter_chunks:
                label = letter_chunk["name"] if letter_chunk["name"] != "" else None
                c.node(
                    letter_chunk["structure_id"],
                    label=label,
                    URL=url(letter_chunk["structure_id"]),
                )
            c.node_attr.update(shape="ellipse", style="filled", color="white")
            for label in sub_graph_labels:
                link_concept = [
                    c for c in concepts if c["structure_id"] == label["parent_concept"]
                ][0]
                link_label = (
                    link_concept["name"].upper()
                    if link_concept["name"] != ""
                    else link_concept["structure_id"]
                )
                c.node(
                    label["structure_id"],
                    label=link_label,
                    URL=url(label["structure_id"]),
                )
            for relation in sub_graph_relations:
                link_concept = [
                    c
                    for c in concepts
                    if c["structure_id"] == relation["parent_concept"]
                ][0]
                link_space = [
                    s
                    for s in conceptual_spaces
                    if s["structure_id"] == relation["conceptual_space"]
                ][0]
                concept_name = (
                    link_concept["name"].upper()
                    if link_concept["name"] != ""
                    else link_concept["structure_id"]
                )
                space_name = (
                    link_space["name"].upper()
                    if link_space["name"] != ""
                    else link_space["structure_id"]
                )
                link_label = f"{concept_name}-{space_name}"
                c.node(
                    relation["structure_id"],
                    label=link_label,
                    URL=url(relation["structure_id"]),
                )
            c.attr(label=space["name"])
    for link in correspondence_args:
        if "Label" in link["structure_id"]:
            view_graph.edge(link["structure_id"], link["start"], label="start")
        if "Relation" in link["structure_id"]:
            view_graph.edge(link["structure_id"], link["start"], label="start")
            view_graph.edge(link["structure_id"], link["end"], label="end")
        if "LetterChunk" in link["structure_id"]:
            for letter_chunk in link["right_branch"]:
                view_graph.edge(link["structure_id"], letter_chunk, label="right")
            for letter_chunk in link["left_branch"]:
                view_graph.edge(link["structure_id"], letter_chunk, label="left")
    correspondence_concept_ids = {
        correspondence["parent_concept"] for correspondence in correspondences
    }
    correspondence_concepts = {
        c: get_structure_json(run_id, c, time) for c in correspondence_concept_ids
    }
    for correspondence in correspondences:
        color = (
            "black"
            if correspondence_concepts[correspondence["parent_concept"]]["name"]
            == "same"
            else "red"
        )
        view_graph.edge(
            correspondence["start"],
            correspondence["end"],
            style="dashed",
            color=color,
        )
    for label1 in labels:
        for label2 in labels:
            if label1 == label2:
                continue
            if label1["parent_concept"] != label2["parent_concept"]:
                continue
            concept = [
                c for c in concepts if c["structure_id"] == label1["parent_concept"]
            ][0]
            if concept["name"] != "":
                continue
            view_graph.edge(
                label1["structure_id"],
                label2["structure_id"],
                style="dashed",
                color="blue",
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
