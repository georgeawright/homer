import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.interpreter import Interpreter


def test_interpret_assignment():
    bubble_chamber = BubbleChamber.setup(Mock())
    interpreter = Interpreter(bubble_chamber)

    assignment_1 = (
        'input=Concept(parent_id:"x";name:"input";locations:[];'
        + "classifier:None;instance_type:None;structure_type:None;"
        + "parent_space:None;distance_function:None;depth:1)"
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
            parent_id:"x"; name:"input"; locations:[]; classifier:None;
            instance_type:None; structure_type:None; parent_space:None;
            distance_function:None; depth:1
        ).
        temperature_concept = Concept(
            parent_id:"x"; name:"temperature"; locations:[]; classifier:None;
            instance_type:None; structure_type:None; parent_space:None;
            distance_function:None; depth:1
        ).
        temperature_space = ConceptualSpace(
            parent_id:"x"; name:"temperature space"; parent_concept:temperature_concept;
            no_of_dimensions:1; dimensions:[]; sub_spaces:[]; is_basic_level:True
        ).
        hot_concept = Concept(
            parent_id:"x"; name:"hot"; locations:[Location([[20]], temperature_space)];
            classifier:ProximityClassifier; instance_type:None; structure_type:None;
            parent_space:temperature_space; distance_function:centroid_euclidean_distance;
            depth:1
        ).
    """

    interpreter.interpret_string(string)

    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0

    temperature_concept = bubble_chamber.concepts["temperature"]
    assert temperature_concept.name == "temperature"
    assert temperature_concept.depth == 1.0

    temperature_space = bubble_chamber.conceptual_spaces["temperature space"]
    assert temperature_space.parent_concept == temperature_concept


def test_interpret_file(tmpdir):
    bubble_chamber = BubbleChamber.setup(Mock())
    interpreter = Interpreter(bubble_chamber)

    test_file = tmpdir.join("test_file")
    with open(test_file.strpath, "w") as f:
        f.write(
            """
            input = Concept(
                parent_id:"x"; name:"input"; locations:[]; classifier:None;
                instance_type:None; structure_type:None; parent_space: None;
                distance_function: None; depth: 1
            ).
            """
        )

    interpreter.interpret_file(test_file.strpath)
    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0
