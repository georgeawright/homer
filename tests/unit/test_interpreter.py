import pytest
from unittest.mock import Mock

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.interpreter import Interpreter


def test_parse():
    loggers = {"activity": Mock(), "structure": Mock(), "errors": Mock()}
    bubble_chamber = BubbleChamber.setup(loggers)
    interpreter = Interpreter(bubble_chamber)

    program = (
        "(define input-concept (def-concept bla blah))\n"
        + "(define input-space (def-contextual-space blu bluh))"
    )
    parse_tree = interpreter.parse(program)

    assert parse_tree == [
        "eval",
        ["define", "input-concept", ["def-concept", "bla", "blah"]],
        ["define", "input-space", ["def-contextual-space", "blu", "bluh"]],
    ]


def test_evaluate():
    loggers = {"activity": Mock(), "structure": Mock(), "errors": Mock()}
    bubble_chamber = BubbleChamber.setup(loggers)
    interpreter = Interpreter(bubble_chamber)

    program = '(define s """hello world""")'
    interpreter.evaluate(interpreter.parse(program))
    assert interpreter.names["s"] == "hello world"

    program = "(define a (list 1 2))"
    interpreter.evaluate(interpreter.parse(program))
    assert interpreter.names["a"] == [1, 2]

    program = '(define b (tuple "k" 1))'
    interpreter.evaluate(interpreter.parse(program))
    assert interpreter.names["b"] == ("k", 1)

    program = '(define c (dict (list (tuple "k" 1))))'
    interpreter.evaluate(interpreter.parse(program))
    assert interpreter.names["c"] == {"k": 1}

    program = '(define d (python """lambda x: x*2"""))'
    interpreter.evaluate(interpreter.parse(program))
    func = interpreter.names["d"]
    assert func(2) == 4


def test_interpret_string():
    loggers = {"activity": Mock(), "structure": Mock(), "errors": Mock()}
    bubble_chamber = BubbleChamber.setup(loggers)
    interpreter = Interpreter(bubble_chamber)

    string = """
    (define input (def-concept :parent_id "x" :name "input" :locations (list) :classifier None :instance_type None :structure_type None :parent_space None :distance_function None :depth 1))
    (define temperature_concept (def-concept :parent_id "x" :name "temperature" :locations (list) :classifier None :instance_type None :structure_type None :parent_space None :distance_function None :depth 1))
    (define temperature_space (def-conceptual-space :parent_id "x" :name "temperature" :parent_concept temperature_concept :no_of_dimensions 1 :dimensions (list) :sub_spaces (list) :is_basic_level True))
    (define hot_concept (def-concept :parent_id "x" :name "hot" :locations (list (Location (list(list 20)) temperature_space)) :classifier ProximityClassifier :instance_type Chunk :structure_type Label :parent_space temperature_space :distance_function centroid_euclidean_distance :depth 1))
    """

    interpreter.interpret_string(string)

    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0

    temperature_concept = bubble_chamber.concepts["temperature"]
    assert temperature_concept.name == "temperature"
    assert temperature_concept.depth == 1.0

    temperature_space = bubble_chamber.conceptual_spaces["temperature"]
    assert temperature_space.parent_concept == temperature_concept


def test_interpret_file(tmpdir):
    loggers = {"activity": Mock(), "structure": Mock(), "errors": Mock()}
    bubble_chamber = BubbleChamber.setup(loggers)
    interpreter = Interpreter(bubble_chamber)

    test_file = tmpdir.join("test_file")
    with open(test_file.strpath, "w") as f:
        f.write(
            """(define input (def-concept :parent_id "x" :name "input" :locations (list) :classifier None :instance_type None :structure_type None :parent_space None :distance_function None :depth 1))
            """
        )

    interpreter.interpret_file(test_file.strpath)
    input_concept = bubble_chamber.concepts["input"]
    assert input_concept.name == "input"
    assert input_concept.depth == 1.0
