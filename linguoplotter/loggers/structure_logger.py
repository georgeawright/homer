import json
import math
import os

from linguoplotter.logger import Logger
from linguoplotter.structure_collection import StructureCollection


class StructureLogger(Logger):
    def __init__(self, directory: str, coderack: "Coderack" = None):
        self.directory = directory if directory[-1] != "/" else directory[:-1]
        self.coderack = coderack

    def log(self, structure):
        codelets_run = self.coderack.codelets_run
        structures_directory = f"{self.directory}/structures"
        directory = f"{structures_directory}/{structure.structure_id}"
        try:
            os.mkdir(structures_directory)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        output_file_path = f"{directory}/{codelets_run}.json"
        with open(output_file_path, "w") as f:
            json.dump(structure.__dict__(), f, sort_keys=False, indent=4)

        pass

    def log_concepts_and_frames(self, bubble_chamber, coderack):
        """output dot file of concepts, frames, connections, and activations"""
        codelets_run = coderack.codelets_run
        concepts_directory = f"{self.directory}/concepts_and_frames"
        try:
            os.mkdir(concepts_directory)
        except FileExistsError:
            pass
        output_file_path = f"{concepts_directory}/{codelets_run}.dot"
        with open(output_file_path, "w") as f:
            f.write("digraph G {\n")
            space_count = 0
            graphed_nodes = {}
            for space in bubble_chamber.conceptual_spaces.where(is_slot=False):
                nodes = space.contents.filter(
                    lambda x: not x.is_slot
                    and (x.is_concept or x.is_letter_chunk)
                    and x.parent_space == space
                )
                if nodes.is_empty():
                    continue
                f.write(f"subgraph cluster_{space_count} {{\n")
                f.write("style=filled; color=pink; node [style=filled, color=white];\n")
                for node in nodes:
                    node_name = (
                        node.name.upper() if node.is_concept else node.name.lower()
                    )
                    node_size = self._activation_to_font_size(node.activation)
                    f.write(
                        f'{node.structure_id} [label="{node_name}" fontsize={node_size}];\n'
                    )
                    graphed_nodes[node] = True
                space_name = space.name.upper()
                f.write(f'label="{space_name}";\n')
                f.write("}\n")
                space_count += 1
            f.write(f"subgraph cluster_{space_count} {{\n")
            f.write(
                "style=filled; color=lightblue; node [style=filled, color=white];\n"
            )
            for frame in bubble_chamber.frames:
                node_name = frame.name
                node_size = self._activation_to_font_size(frame.activation)
                f.write(
                    f'{frame.structure_id} [label="{node_name}" fontsize={node_size}];\n'
                )
                graphed_nodes[frame] = True
            f.write('label="frames";\n')
            f.write("}\n")
            for node in graphed_nodes:
                for link in node.links_out.filter(
                    lambda x: x.start in graphed_nodes and x.end in graphed_nodes
                ):
                    start_id = link.start.structure_id
                    end_id = link.end.structure_id
                    label_name = (
                        link.parent_concept.name.upper()
                        if link.parent_concept is not None
                        else ""
                    )
                    color_number = math.ceil((1 - link.activation) * 200)
                    color_hex = hex(color_number)[2:]
                    if len(color_hex) == 1:
                        color_hex = "0" + color_hex
                    color_code = "#" + color_hex * 3
                    f.write(
                        f"{start_id} -> {end_id} "
                        + f'[label="{label_name}", color="{color_code}"];\n'
                    )
                if node.is_frame:
                    for instance in node.instances:
                        f.write(
                            f"{node.structure_id} -> {instance.structure_id} "
                            + '[label="instance", color="#000000"]\n'
                        )
            f.write("}\n")

    def log_contextual_space(self, space, coderack):
        """output dot file of nodes and links in contextual space"""
        codelets_run = coderack.codelets_run
        spaces_directory = f"{self.directory}/spaces"
        directory = f"{spaces_directory}/{space.structure_id}"
        try:
            os.mkdir(spaces_directory)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        output_file_path = f"{directory}/{codelets_run}.dot"
        with open(output_file_path, "w") as f:
            f.write("digraph G {\n")
            f.write("subgraph cluster_0 {\n")
            f.write(
                "style=filled; color=lightblue; node [style=filled, color=white];\n"
            )
            for item in space.contents.where(is_correspondence=False):
                if item.is_node:
                    item_name = (
                        item.name if hasattr(item, "name") else item.structure_id
                    )
                else:
                    item_name = (
                        item.parent_concept.name.upper()
                        if item.parent_concept is not None
                        else item.structure_id
                    )
                item_size = self._activation_to_font_size(item.activation)
                f.write(
                    f'{item.structure_id} [label="{item_name}" fontsize={item_size}];\n'
                )
            for item in space.contents.where(is_correspondence=False):
                if item.is_node:
                    for left_node in item.left_branch:
                        f.write(
                            f"{item.structure_id} -> {left_node.structure_id} "
                            + '[label="left"];\n'
                        )
                    for right_node in item.right_branch:
                        f.write(
                            f"{item.structure_id} -> {right_node.structure_id} "
                            + '[label="left"];\n'
                        )
                else:
                    f.write(
                        f'{item.structure_id} -> {item.start.structure_id} [label="start"];\n'
                    )
                    if item.end is not None:
                        f.write(
                            f'{item.structure_id} -> {item.end.structure_id} [label="end"];\n'
                        )
            f.write(f'label="{space.structure_id}";\n')
            f.write("}\n")
            f.write("}\n")

    def log_view(self, view):
        self.log_view_json(view)
        self.log_view_dot(view)

    def log_view_json(self, view):
        codelets_run = self.coderack.codelets_run
        views_directory = f"{self.directory}/views"
        directory = f"{views_directory}/{view.structure_id}"
        try:
            os.mkdir(views_directory)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        output_file_path = f"{directory}/{codelets_run}.json"
        with open(output_file_path, "w") as f:
            json.dump(view.__dict__(), f, sort_keys=False, indent=4)

    def log_view_dot(self, view):
        def log_space(
            f, space, cluster_count, background_color, space_type: str = "input"
        ):
            f.write(f"subgraph cluster_{cluster_count} {{\n")
            f.write(
                f"style=filled; color={background_color}; "
                + "node [style=filled, color=white];\n"
            )
            for node in space.contents.filter(
                lambda x: x.is_node
                and (x in view.grouped_nodes or space_type == "output")
            ):
                node_label = (
                    node.name
                    if node.is_letter_chunk and node.name is not None
                    else node.structure_id
                )
                f.write(f'{node.structure_id} [label="{node_label}"];\n')
            for letter_chunk in space.contents.filter(
                lambda x: x.is_letter_chunk
                and (x in view.grouped_nodes or space_type == "output")
            ):
                for left_member in letter_chunk.left_branch:
                    f.write(
                        f"{letter_chunk.structure_id} -> "
                        + f'{left_member.structure_id} [label="left"];\n'
                    )
                for right_member in letter_chunk.right_branch:
                    f.write(
                        f"{letter_chunk.structure_id} -> "
                        + f'{right_member.structure_id} [label="right"];\n'
                    )
            for label in space.contents.filter(
                lambda x: x.is_label and x.has_correspondence_in_view(view)
            ):
                concept_label = (
                    label.parent_concept.name
                    if not label.parent_concept.is_slot
                    else label.structure_id
                )
                f.write(f'{label.structure_id} [label="{concept_label}"];\n')
                f.write(
                    f"{label.structure_id} -> "
                    + f'{label.start.structure_id} [label="start"];\n'
                )
            for relation in space.contents.filter(
                lambda x: x.is_relation and x.has_correspondence_in_view(view)
            ):
                concept_label = (
                    relation.parent_concept.name
                    if not relation.parent_concept.is_slot
                    else relation.structure_id
                )
                f.write(f'{relation.structure_id} [label="{concept_label}"];\n')
                f.write(
                    f"{relation.structure_id} -> "
                    + f'{relation.start.structure_id} [label="start"];\n'
                )
                f.write(
                    f"{relation.structure_id} -> "
                    + f'{relation.end.structure_id} [label="end"];\n'
                )
            f.write(f'label = "{space.structure_id}";\n')
            f.write("}")

        codelets_run = self.coderack.codelets_run
        views_directory = f"{self.directory}/views"
        directory = f"{views_directory}/{view.structure_id}"
        try:
            os.mkdir(views_directory)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        output_file_path = f"{directory}/{codelets_run}.dot"
        with open(output_file_path, "w") as f:
            f.write("digraph G {\n")
            cluster_count = 0
            for space in view.input_spaces:
                log_space(f, space, cluster_count, "lightblue")
                cluster_count += 1
            log_space(
                f, view.output_space, cluster_count, "palegreen", space_type="output"
            )
            cluster_count += 1
            f.write(f"subgraph cluster_{cluster_count} {{\n")
            f.write(
                "style=filled; color=lightgray; node [style=filled, color=white];\n"
            )
            cluster_count += 1
            f.write(f"subgraph cluster_{cluster_count} {{\n")
            f.write("style=filled; color=pink; node [style=filled, color=white];\n")
            for concept in view.parent_frame.concepts.where(is_concept=True):
                f.write(f"{concept.structure_id};\n")
            for concept in view.parent_frame.concepts.where(is_concept=True):
                for relation in concept.links_out.filter(
                    lambda x: x.is_relation and x.end in view.parent_frame.concepts
                ):
                    f.write(
                        f"{relation.structure_id} "
                        + f'[label="{relation.parent_concept.name}"];\n'
                    )
                    f.write(
                        f"{relation.structure_id} -> "
                        + f'{relation.start.structure_id} [label="start"];\n'
                    )
                    f.write(
                        f"{relation.structure_id} -> "
                        + f'{relation.end.structure_id} [label="end"];\n'
                    )
            f.write('label = "Concepts";\n')
            f.write("}\n")
            cluster_count += 1
            log_space(f, view.parent_frame.input_space, cluster_count, "lightblue")
            cluster_count += 1
            log_space(
                f,
                view.parent_frame.output_space,
                cluster_count,
                "palegreen",
                space_type="output",
            )
            for link in StructureCollection.union(
                view.parent_frame.input_space.contents,
                view.parent_frame.output_space.contents,
            ).filter(lambda x: x.is_label or x.is_relation):
                if link.parent_concept in view.parent_frame.concepts:
                    f.write(
                        f"{link.structure_id} -> "
                        + f"{link.parent_concept.structure_id} "
                        + '[label="parent_concept"];\n'
                    )
            f.write(f'label = "{view.parent_frame.structure_id}";\n')
            f.write("}\n")
            for correspondence in view.members:
                if (
                    correspondence.start.parent_space in view.input_spaces
                    or correspondence.start in view.parent_frame.output_space.contents
                ) and (
                    correspondence.end in view.parent_frame.input_space.contents
                    or correspondence.end in view.output_space.contents
                ):
                    f.write(
                        f"{correspondence.structure_id} "
                        + f'[label="{correspondence.parent_concept.name}"];\n'
                    )
                    f.write(
                        f"{correspondence.structure_id} -> "
                        + f"{correspondence.start.structure_id};\n"
                    )
                    f.write(
                        f"{correspondence.structure_id} -> "
                        + f"{correspondence.end.structure_id};\n"
                    )
            f.write("}\n")

    def log_structure(self, structure):
        """output json file of structure attributes"""

    def _activation_to_font_size(self, activation):
        return activation * 30 + 10
