import json
import pathlib

from linguoplotter.logger import Logger


class ActivityLogger(Logger):
    def __init__(
        self,
        codelets_directory: str,
        satisfaction_stream=None,
        determinism_stream=None,
        coderack_population_stream=None,
        view_count_stream=None,
        codelet_spawned_stream=None,
        codelet_run_stream=None,
    ):
        self.codelets_directory = codelets_directory
        self.satisfaction_stream = satisfaction_stream
        self.determinism_stream = determinism_stream
        self.coderack_population_stream = coderack_population_stream
        self.view_count_stream = view_count_stream
        self.codelet_spawned_stream = codelet_spawned_stream
        self.codelet_run_stream = codelet_run_stream
        self.codelet = None
        self.codelet_json = None
        self.codelets_run = 0
        self.log_files_count = 0
        self.LOG_LENGTH = 1000
        self.LINE_WIDTH = 120

    def log(self, message: str):
        self.codelet_json["activity"].append(message)
        return self

    def log_dict(self, dictionary, name: str = None):
        name = dictionary.name if name is None else name
        self.codelet_json["activity"].append(name)
        self.codelet_json["activity"].append(dictionary.__dict__())
        return self

    def log_set(self, structure_set, name: str = None):
        name = structure_set.name if name is None else name
        self.codelet_json["activity"].append(name)
        self.codelet_json["activity"].append(structure_set.__dict__())
        return self

    def log_list(self, structure_list, name: str = None):
        name = structure_list.name if name is None else name
        self.codelet_json["activity"].append(name)
        self.codelet_json["activity"].append(structure_list.__dict__())
        return self

    def log_codelet_start(self, codelet: "Codelet"):
        self.codelet = codelet
        self.codelets_run += 1
        self.codelet_json = {}
        self.codelet_log_file = (
            f"{self.codelets_directory}/times/{self.codelets_run}.json"
        )
        self.codelet_json["id"] = self.codelet.codelet_id
        self.codelet_json["parent_id"] = self.codelet.parent_id
        self.codelet_json["targets"] = self.codelet.targets.__dict__()
        self.codelet_json["urgency"] = self.codelet.urgency
        self.codelet_json["time"] = self.codelets_run
        self.codelet_json["activity"] = []
        return self

    def log_codelet_end(self, coderack_population: int):
        codelet_log_file = f"{self.codelets_directory}/times/{self.codelets_run}.json"
        pathlib.Path(
            f"{self.codelets_directory}/ids/{self.codelet.codelet_id}.json"
        ).symlink_to(self.codelet_log_file)
        self.codelet_json["satisfaction"] = self.codelet.bubble_chamber.satisfaction
        self.codelet_json["coderack_population"] = coderack_population
        self.codelet_json["view_count"] = len(self.codelet.bubble_chamber.views)
        self.codelet_json["focus"] = (
            self.codelet.bubble_chamber.focus.view.structure_id
            if self.codelet.bubble_chamber.focus.view is not None
            else None
        )
        self.codelet_json["worldview"] = (
            self.codelet.bubble_chamber.worldview.view.structure_id
            if self.codelet.bubble_chamber.worldview.view is not None
            else None
        )
        self.codelet_json["child_structures"] = (
            [s.structure_id for s in self.codelet.child_structures]
            if self.codelet.child_structures is not None
            else []
        )
        self.codelet_json["child_codelets"] = [
            c.codelet_id for c in self.codelet.child_codelets
        ]
        self.codelet_json["result"] = self.codelet.result.name
        with open(codelet_log_file, "w") as f:
            json.dump(self.codelet_json, f, sort_keys=False, indent=4)
        self._log_satisfaction()
        self._log_coderack_population(coderack_population)
        self._log_view_count(len(self.codelet.bubble_chamber.views))
        return self

    def _log_satisfaction(self):
        if self.satisfaction_stream is not None:
            self.satisfaction_stream.write(
                f"{self.codelets_run},{self.codelet.bubble_chamber.satisfaction}\n"
            )
        if self.determinism_stream is not None:
            self.determinism_stream.write(
                f"{self.codelets_run},{self.codelet.bubble_chamber.random_machine.determinism}\n"
            )
        return self

    def _log_coderack_population(self, coderack_population: int):
        if self.coderack_population_stream is not None:
            self.coderack_population_stream.write(
                f"{self.codelets_run},{coderack_population}\n"
            )
        return self

    def _log_view_count(self, view_count: int):
        if self.view_count_stream is not None:
            self.view_count_stream.write(f"{self.codelets_run},{view_count}\n")
        return self
