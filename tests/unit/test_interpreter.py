import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.interpreter import Interpreter


def test_interpret_assignment():
    bubble_chamber = BubbleChamber.setup(Mock())
    interpreter = Interpreter(bubble_chamber)

    assignment_1 = (
        'input=Concept(parent_id:"x",name:"input",locations:[],'
        + "classifier:None,instance_type:None,structure_type:None,"
        + "parent_space:None,distance_function:None,depth:1"
    )

    interpreter.interpret_assignment(assignment_1)
    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0


def test_interpret_string():
    bubble_chamber = BubbleChamber.setup(Mock())
    interpreter = Interpreter(bubble_chamber)

    string = """
        input = Concept(
            parent_id:"x", name:"input", locations:[], classifier:None,
            instance_type:None, structure_type:None, parent_space: None,
            distance_function: None, depth: 1
        ).
    """

    interpreter.interpret_string(string)
    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0


def test_interpret_file(tmpdir):
    bubble_chamber = BubbleChamber.setup(Mock())
    interpreter = Interpreter(bubble_chamber)

    test_file = tmpdir.join("test_file")
    with open(test_file.strpath, "w") as f:
        f.write(
            """
            input = Concept(
                parent_id:"x", name:"input", locations:[], classifier:None,
                instance_type:None, structure_type:None, parent_space: None,
                distance_function: None, depth: 1
            ).
            """
        )

    interpreter.interpret_file(test_file.strpath)
    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0
