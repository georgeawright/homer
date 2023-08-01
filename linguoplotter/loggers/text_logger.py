import json
import pathlib

from linguoplotter.logger import Logger


class TextLogger(Logger):
    def __init__(self, hyper_parameters: str, seed: int, program: str, stream):
        self.hyper_parameters = hyper_parameters
        self.seed = seed
        self.program = program
        self.stream = stream

    def log_text(self, time: int, text: str, quality: float):
        self.stream.write(
            f"{self.hyper_parameters},{self.seed},{self.program},{time},{text},{quality}\n"
        )
        return self
