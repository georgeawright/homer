import yaml

from .perceptlets import RawPerceptlet, RawPerceptletField, RawPerceptletFieldSequence


class Problem:

    NEIGHBOUR_RELATIVE_COORDINATES = [
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
    ]

    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    def as_raw_perceptlet_field_sequence(self) -> RawPerceptletFieldSequence:
        with open(self.path_to_file) as f:
            model_input = yaml.load(f, Loader=yaml.FullLoader)
            raw_perceptlets = [
                [
                    RawPerceptlet(cell_value, [0, i, j], set())
                    for j, cell_value in enumerate(row)
                ]
                for i, row in enumerate(model_input)
            ]
            for i, row in enumerate(raw_perceptlets):
                for j, perceptlet in enumerate(row):
                    for x, y in self.NEIGHBOUR_RELATIVE_COORDINATES:
                        if (
                            i + x >= 0
                            and i + x < len(raw_perceptlets)
                            and j + y >= 0
                            and j + y < len(row)
                        ):
                            perceptlet.neighbours.add(raw_perceptlets[i + x][j + y])

            raw_perceptlet_field = RawPerceptletField(raw_perceptlets, 0, set())
            raw_perceptlet_field_sequence = RawPerceptletFieldSequence(
                [raw_perceptlet_field]
            )
        return raw_perceptlet_field_sequence
