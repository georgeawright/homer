from __future__ import annotations
import csv
import os
import time
from typing import Any, List

from graphviz import Digraph
from matplotlib import pyplot


class Logger:
    def __init__(self, log_directory: str = "logs"):
        self.log_directory = log_directory
        self.codelets_run = 0

    @classmethod
    def setup(cls, path_to_logs: str) -> Logger:
        if not os.path.exists(path_to_logs):
            os.makedirs(path_to_logs)
        now = time.localtime()
        logging_directory = (
            path_to_logs
            + "/"
            + str(now.tm_year)
            + str(now.tm_mon)
            + str(now.tm_mday)
            + str(now.tm_hour)
            + str(now.tm_min)
            + str(now.tm_sec)
        )
        os.makedirs(logging_directory)
        os.makedirs(logging_directory + "/concepts")
        logger = Logger(logging_directory)
        return logger

    def log(self, item: Any):
        from homer.codelet import Codelet
        from homer.coderack import Coderack
        from homer.concept import Concept
        from homer.perceptlet import Perceptlet

        if isinstance(item, str):
            return self._log_message(item)
        if isinstance(item, Codelet):
            return self._log_codelet(item)
        if isinstance(item, Coderack):
            return self._log_coderack(item)
        if isinstance(item, Concept):
            return self._log_concept(item)
        if isinstance(item, Perceptlet):
            return self._log_perceptlet(item)

    def _log_message(self, message):
        print(message)
        messages_file = self.log_directory + "/messages.txt"
        with open(messages_file, "a") as f:
            f.write(message + "\n")

    def _log_codelet(self, codelet):
        """log the birth of a codelet"""
        codelet_type_name = type(codelet).__name__
        self._log_message(
            f"    + {codelet_type_name} spawned - urgency: {codelet.urgency}"
        )
        codelets_file = self.log_directory + "/codelets.csv"
        with open(codelets_file, "a") as f:
            codelet_id = "CodeletID"
            parent_id = "ParentID"
            birth_time = "BirthTime"
            codelet_type = "CodeletType"
            writer = csv.DictWriter(
                f, [codelet_id, parent_id, birth_time, codelet_type]
            )
            writer.writerow(
                {
                    codelet_id: codelet.codelet_id,
                    parent_id: codelet.parent_id,
                    birth_time: self.codelets_run,
                    codelet_type: type(codelet),
                }
            )

    def _log_coderack(self, coderack):
        """log the coderack status"""
        coderack_file = self.log_directory + "/coderack.csv"
        self.codelets_run = coderack.codelets_run
        with open(coderack_file, "a") as f:
            codelets_run = "CodeletsRun"
            coderack_population = "CoderackPopulation"
            writer = csv.DictWriter(f, [codelets_run, coderack_population])
            writer.writerow(
                {
                    codelets_run: self.codelets_run,
                    coderack_population: len(coderack._codelets),
                }
            )

    def _log_concept(self, concept):
        """log the activation of a concept"""
        concept_file = self.log_directory + "/concepts/" + concept.name + ".csv"
        with open(concept_file, "a") as f:
            codelets_run = "CodeletsRun"
            activation = "Activation"
            writer = csv.DictWriter(f, [codelets_run, activation])
            writer.writerow(
                {
                    codelets_run: self.codelets_run,
                    activation: concept.get_activation_as_scalar(),
                }
            )

    def _log_perceptlet(self, perceptlet):
        """log the creation of a perceptlet"""
        perceptlet_type_name = type(perceptlet).__name__
        self._log_message(
            f"{perceptlet_type_name} created - value: {perceptlet.value} "
            + f"location: {perceptlet.location}; strength: {perceptlet.strength}"
        )
        perceptlets_file = self.log_directory + "/perceptlets.csv"
        with open(perceptlets_file, "a") as f:
            perceptlet_id = "PerceptletID"
            parent_id = "ParentID"
            perceptlet_type = "PerceptletType"
            birth_time = "BirthTime"
            location = "Location"
            value = "Value"
            size = "Size"
            writer = csv.DictWriter(
                f,
                [
                    perceptlet_id,
                    parent_id,
                    perceptlet_type,
                    birth_time,
                    location,
                    value,
                    size,
                ],
            )
            writer.writerow(
                {
                    perceptlet_id: perceptlet.perceptlet_id,
                    parent_id: perceptlet.parent_id,
                    perceptlet_type: perceptlet_type_name,
                    birth_time: self.codelets_run,
                    location: perceptlet.location,
                    value: perceptlet.value,
                    size: perceptlet.size,
                }
            )

    def graph_concepts(self, concept_names: List[str], file_name: str):
        for concept_name in concept_names:
            concept_file = self.log_directory + "/concepts/" + concept_name + ".csv"
            if not os.path.exists(concept_file):
                print(f"No activation data for {concept_name}")
                continue
            with open(concept_file, "r") as f:
                data = list(csv.reader(f))
                x = [float(element[0]) for element in data]
                y = [float(element[1]) for element in data]
                pyplot.plot(x, y, label=concept_name)
        pyplot.xlabel("Codelets Run")
        pyplot.ylabel("Activation")
        pyplot.legend(loc="best")
        pyplot.savefig(f"{self.log_directory}/{file_name}.png")

    def graph_codelets(self, file_name: str):
        family_tree = Digraph(
            "Codelets",
            filename=file_name,
            node_attr={"color": "lightblue2", "style": "filled"},
        )
        family_tree.attr(size="6, 6")
        codelets_file = self.log_directory + "/codelets.csv"
        with open(codelets_file, "r") as f:
            data = list(csv.reader(f))
            for row in data:
                family_tree.edge(row[0], row[1])
        family_tree.view()
