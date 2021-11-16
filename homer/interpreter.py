import re

from .location import Location


class Interpreter:
    def __init__(self, bubble_chamber):
        self.bubble_chamber = bubble_chamber
        self.names = {}
        self.object_methods = {"Concept": "new_concept"}

    def interpret_assignment(self, assignment: str):
        operands = assignment.split("=")
        name = operands[0]
        definition = operands[1]
        type_name = definition.split("(")[0]
        arguments = definition.split("(")[1].split(")")[0]
        arguments_list = arguments.split(",")
        arguments_dict = {}
        for argument in arguments_list:
            pairs = argument.split(":")
            key = pairs[0]
            value = pairs[1]
            arguments_dict[key] = self._pythonize_value(value)
        object_method_name = self.object_methods[type_name]
        method = getattr(self.bubble_chamber, object_method_name)
        self.names[name] = method(**arguments_dict)

    def interpret_string(self, string: str):
        string = re.sub(r"\s+", "", string)
        assignments = string.split(".")
        for assignment in assignments:
            if assignment == "":
                continue
            self.interpret_assignment(assignment)

    def interpret_file(self, file_name: str):
        with open(file_name, "r") as f:
            current_assignment = ""
            while True:
                character = f.read(1)
                if not character:
                    if current_assignment != "":
                        raise Exception("Unexpected EOF")
                    break
                if character == ".":
                    self.interpret_assignment(current_assignment)
                    current_assignment = ""
                else:
                    current_assignment += re.sub(r"\s", "", character)

    def _pythonize_value(self, value: str):
        if value[0] == "[":
            elements = value[1 : len(value) - 1].split(",")
            return [
                self._pythonize_value(element) for element in elements if element != ""
            ]
        if value[0] in {'"', "'"}:
            return value[1:-1]
        if value in self.names:
            return self.names[value]
        if "Location(" in value:
            arguments = value.split("(")[1].split(")")[0].split(",")
            pythonized_arguments = [self._pythonize_value(arg) for arg in arguments]
            return Location(*pythonized_arguments)
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
