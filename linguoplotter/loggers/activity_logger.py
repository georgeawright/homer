from linguoplotter.codelet_result import CodeletResult
from linguoplotter.logger import Logger


class ActivityLogger(Logger):
    def __init__(
        self,
        log_file_name: str,
        satisfaction_stream=None,
        coderack_population_stream=None,
        view_count_stream=None,
        codelet_spawned_stream=None,
        codelet_run_stream=None,
    ):
        self.log_file_name = log_file_name
        self.satisfaction_stream = satisfaction_stream
        self.coderack_population_stream = coderack_population_stream
        self.view_count_stream = view_count_stream
        self.codelet_spawned_stream = codelet_spawned_stream
        self.codelet_run_stream = codelet_run_stream
        self._stream = None
        self.codelet = None
        self.codelets_run = 0
        self.log_files_count = 0
        self.LOG_LENGTH = 1000
        self.LINE_WIDTH = 120

    @property
    def stream(self):
        if self.log_files_count == 0:
            self.log_files_count += 1
            new_log_file_name = f"{self.log_file_name}{self.log_files_count}.log"
            self._stream = open(new_log_file_name, "w")
        elif self.codelets_run // self.log_files_count > self.LOG_LENGTH:
            self._stream.close()
            self.log_files_count += 1
            new_log_file_name = f"{self.log_file_name}{self.log_files_count}.log"
            self._stream = open(new_log_file_name, "w")
        return self._stream

    def log(self, message: str):
        self.stream.write(f"{message}\n")

    def log_codelet_spawned(self, codelet: "Codelet"):
        if self.codelet_spawned_stream is not None:
            self.codelet_spawned_stream.write(
                f"{self.codelets_run},{codelet.codelet_id},{codelet.urgency}\n"
            )

    def log_codelet_run(self, codelet: "Codelet"):
        if self.codelet_run_stream is not None:
            self.codelet_run_stream.write(
                f"{self.codelets_run},{codelet.codelet_id},{codelet.urgency}\n"
            )

    def log_dict(self, dictionary, name: str = None):
        name = dictionary.name if name is None else name
        if dictionary is None or len(dictionary) == 0:
            self.log("No " + name.lower())
        else:
            self.log(f"{name}: {{")
            for key, value in dictionary.items():
                self.log(f"    {key}: {value},")
            self.log("}")

    def log_set(self, structure_set, name: str = None):
        name = structure_set.name if name is None else name
        if structure_set is None or len(structure_set) == 0:
            self.log("No " + name.lower())
        else:
            self.log(f"{name}: {{")
            for item in structure_set:
                self.log(f"    {item},")
            self.log("}")

    def log_list(self, structure_list, name: str = None):
        name = structure_list.name if name is None else name
        if structure_list is None or len(structure_list) == 0:
            self.log("No " + name.lower())
        else:
            self.log(f"{name}: [")
            for item in structure_list:
                self.log(f"    {item},")
            self.log("]")

    def log_codelet_start(self, codelet: "Codelet"):
        self.codelet = codelet
        self.codelets_run += 1
        codelet_title = f" Codelet run {self.codelets_run}: {codelet.codelet_id} "
        no_of_dashes = (self.LINE_WIDTH - len(codelet_title)) // 2
        codelet_title = "-" * no_of_dashes + codelet_title + "-" * no_of_dashes
        if len(codelet_title) < self.LINE_WIDTH:
            codelet_title += "-"
        self.stream.write(f"\n{codelet_title}\n")
        self.stream.write(f"Parent: {codelet.parent_id} | Urgency: {codelet.urgency}\n")

    def log_codelet_end(self, coderack_population: int):
        if hasattr(self.codelet, "child_structures"):
            self.log_list(self.codelet.child_structures, "Child structures")
        self.log_set(self.codelet.child_codelets, "Follow ups")
        if CodeletResult.FINISH == self.codelet.result:
            self.log("Result: FINISH")
        if CodeletResult.FIZZLE == self.codelet.result:
            self.log("Result: FIZZLE")
        self.log("-" * self.LINE_WIDTH)
        self.log(
            f"Time: {self.codelets_run} | "
            + f"Satisfaction: {self.codelet.bubble_chamber.satisfaction} | "
            + f"Coderack Population Size: {coderack_population} | "
            + f"View Count: {len(self.codelet.bubble_chamber.views)}\n"
            + f"Focus: {self.codelet.bubble_chamber.focus.view}\n"
            + f"Worldview: {self.codelet.bubble_chamber.worldview.view}\n",
        )
        self._log_satisfaction()
        self._log_coderack_population(coderack_population)
        self._log_view_count(len(self.codelet.bubble_chamber.views))

    def _log_satisfaction(self):
        if self.satisfaction_stream is not None:
            self.satisfaction_stream.write(
                f"{self.codelets_run},{self.codelet.bubble_chamber.satisfaction}\n"
            )

    def _log_coderack_population(self, coderack_population: int):
        if self.coderack_population_stream is not None:
            self.coderack_population_stream.write(
                f"{self.codelets_run},{coderack_population}\n"
            )

    def _log_view_count(self, view_count: int):
        if self.view_count_stream is not None:
            self.view_count_stream.write(f"{self.codelets_run},{view_count}\n")
