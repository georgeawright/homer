import re

from . import classifiers
from .location import Location
from .tools import centroid_euclidean_distance


class Interpreter:
    def __init__(self, bubble_chamber):
        self.bubble_chamber = bubble_chamber
        self.names = {}
        self.classifiers = {
            "DifferenceClassifier": classifiers.DifferenceClassifier,
            "DifferentnessClassifier": classifiers.DifferentnessClassifier,
            "ProximityClassifier": classifiers.ProximityClassifier,
            "SamenessClassifier": classifiers.SamenessClassifier,
        }
        self.distance_functions = {
            "centroid_euclidean_distance": centroid_euclidean_distance
        }
        self.object_methods = {
            "ConceptualSpace": bubble_chamber.new_conceptual_space,
            "ContextualSpace": bubble_chamber.new_contextual_space,
            "Frame": bubble_chamber.new_frame,
            "Chunk": bubble_chamber.new_chunk,
            "Concept": bubble_chamber.new_concept,
            "LetterChunk": bubble_chamber.new_letter_chunk,
            "Rule": bubble_chamber.new_rule,
            "Correspondence": bubble_chamber.new_correspondence,
            "Label": bubble_chamber.new_label,
            "Relation": bubble_chamber.new_relation,
        }

    def interpret_assignment(self, assignment: str):
        operands = assignment.split("=")
        name = operands[0]
        definition = operands[1]
        arguments_index = definition.index("(")
        type_name = definition[:arguments_index]
        arguments = definition[arguments_index + 1 : len(definition) - 1]
        arguments_list = arguments.split(";")
        arguments_dict = {}
        for argument in arguments_list:
            pairs = argument.split(":")
            key = pairs[0]
            value = pairs[1]
            arguments_dict[key] = self._pythonize_value(value)
        object_method = self.object_methods[type_name]
        self.names[name] = object_method(**arguments_dict)

    def interpret_string(self, string: str):
        current_assignment = ""
        in_string = False
        for character in string:
            if character == ".":
                if in_string:
                    raise Exception("String left open")
                self.interpret_assignment(current_assignment)
                current_assignment = ""
            else:
                if character == '"':
                    in_string = not in_string
                current_assignment += (
                    re.sub(r"\s", "", character) if not in_string else character
                )
        if current_assignment != "":
            raise Exception("Unexpected EOF")

    def interpret_file(self, file_name: str):
        with open(file_name, "r") as f:
            current_assignment = ""
            in_string = False
            while True:
                character = f.read(1)
                if not character:
                    if current_assignment != "":
                        raise Exception("Unexpected EOF")
                    break
                if character == ".":
                    if in_string:
                        raise Exception("String left open")
                    self.interpret_assignment(current_assignment)
                    current_assignment = ""
                else:
                    if character == '"':
                        in_string = not in_string
                    current_assignment += (
                        re.sub(r"\s", "", character) if not in_string else character
                    )

    def _pythonize_value(self, value: str):
        if value[0] == "[":
            elements = []
            in_list = False
            in_function = False
            current_element = ""
            for character in value[1:]:
                if character in {"[", "]"}:
                    in_list = not in_list
                if character in {"(", ")"}:
                    in_function = not in_function
                if character == "," and not in_list and not in_function:
                    elements.append(current_element)
                    current_element = ""
                else:
                    current_element += character
            return [
                self._pythonize_value(element) for element in elements if element != ""
            ]
        if value[0] in {'"', "'"}:
            return value[1:-1]
        if value in self.names:
            return self.names[value]
        if value in self.classifiers:
            return self.classifiers[value]()
        if value in self.distance_functions:
            return self.distance_functions[value]
        if "Location(" in value:
            arguments = value.split("(")[1].split(")")[0].split(",")
            pythonized_arguments = [self._pythonize_value(arg) for arg in arguments]
            return Location(*pythonized_arguments)
        if "StructureCollection(" in value:
            arguments = value.split("(")[1].split(")")[0].split(",")
            pythonized_arguments = [self._pythonize_value(arg) for arg in arguments]
            return self.bubble_chamber.new_structure_collection(*pythonized_arguments)
        if value == "None":
            return None
        if value == "True":
            return True
        if value == "False":
            return False
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            raise Exception(f"Undefined value: {value}.")
