import csv
from typing import Any


class Logger:
    def __init__(self, log_directory: str = "logs"):
        self.log_directory = log_directory
        self.codelets_run = 0

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
        messages_file = self.log_directory + "/messages.txt"
        with open(messages_file, "a") as f:
            f.write(message + "\n")

    def _log_codelet(self, codelet):
        """log the birth of a codelet"""
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
                    coderack_population: len(coderack.codelets),
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
        perceptlets_file = self.log_directory + "/perceptlets.csv"
        with open(perceptlets_file, "a") as f:
            perceptlet_id = "PerceptletID"
            perceptlet_type = "PerceptletType"
            birth_time = "BirthTime"
            location = "Location"
            value = "Value"
            size = "Size"
            writer = csv.DictWriter(
                f, [perceptlet_id, perceptlet_type, birth_time, location, value, size]
            )
            writer.writerow(
                {
                    perceptlet_id: perceptlet.perceptlet_id,
                    perceptlet_type: type(perceptlet),
                    birth_time: self.codelets_run,
                    location: perceptlet.location,
                    value: perceptlet.value,
                    size: perceptlet.size,
                }
            )
