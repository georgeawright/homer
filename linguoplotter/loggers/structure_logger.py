import json
import os

from linguoplotter.logger import Logger


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

    def log_view(self, view):
        self.log_view_json(view)

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
