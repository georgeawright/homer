import re

from . import classifiers
from . import structures
from .location import Location
from .tools import centroid_euclidean_distance

# strings can't contain spaces


class Interpreter:
    def __init__(self, bubble_chamber):
        self.bubble_chamber = bubble_chamber
        self.names = {
            # Structure Types
            "Correspondence": structures.links.Correspondence,
            "Label": structures.links.Label,
            "Relation": structures.links.Relation,
            "Chunk": structures.nodes.Chunk,
            "LetterChunk": structures.nodes.chunks.LetterChunk,
            # Classifier Types
            "DifferenceClassifier": classifiers.DifferenceClassifier,
            "DifferentnessClassifier": classifiers.DifferentnessClassifier,
            "ProximityClassifier": classifiers.ProximityClassifier,
            "SamenessClassifier": classifiers.SamenessClassifier,
            # Distance Functions
            "centroid-euclidean-distance": centroid_euclidean_distance,
            # Structure Factory Methods
            "def-conceptual-space": bubble_chamber.new_conceptual_space,
            "def-contextual-space": bubble_chamber.new_contextual_space,
            "def-frame": bubble_chamber.new_frame,
            "def-chunk": bubble_chamber.new_chunk,
            "def-concept": bubble_chamber.new_concept,
            "def-letter-chunk": bubble_chamber.new_letter_chunk,
            "def-rule": bubble_chamber.new_rule,
            "def-correspondence": bubble_chamber.new_correspondence,
            "def-label": bubble_chamber.new_label,
            "def-relation": bubble_chamber.new_relation,
            # Other inbuilt classes and functions
            "eval": lambda *x: x[-1],
            "list": lambda *x: list(x),
            "Location": Location,
            "None": None,
            "True": True,
            "False": False,
        }

    def parse(self, program: str) -> list:
        program = f"(eval {program})"
        return self.read_from_tokens(self.tokenize(program))

    def tokenize(self, string: str) -> list:
        return string.replace("(", " ( ").replace(")", " ) ").split()

    def read_from_tokens(self, tokens: list):
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF")
        token = tokens.pop(0)
        if token == "(":
            l = []
            while tokens[0] != ")":
                l.append(self.read_from_tokens(tokens))
            tokens.pop(0)
            return l
        elif token == ")":
            raise SyntaxError("Unexpected )")
        else:
            return self.atom(token)

    def atom(self, token: str):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token

    def evaluate(self, x):
        if isinstance(x, str):
            if x[0] == '"':
                return x[1:-1]
            return self.names[x]
        if isinstance(x, (float, int)):
            return x
        if x[0] == "define":
            (_, symbol, exp) = x
            self.names[symbol] = self.evaluate(exp)
        else:
            procedure = self.evaluate(x.pop(0))
            args = []
            while len(x) > 0 and (isinstance(x[0], (float, int)) or x[0][0] != ":"):
                args.append(self.evaluate(x.pop(0)))
            kwargs = {}
            while len(x) > 1:
                key = x.pop(0)[1:]
                value = x.pop(0)
                kwargs[key] = self.evaluate(value)
            if len(x) > 0:
                raise SyntaxError("Positional argument after keyword argument.")
            print("proc", procedure)
            return procedure(*args, **kwargs)

    def interpret_string(self, string: str):
        return self.evaluate(self.parse(string))

    def interpret_file(self, file_name: str):
        with open(file_name, "r") as f:
            self.interpret_string(f.read())
