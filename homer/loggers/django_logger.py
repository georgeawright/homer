from __future__ import annotations

import django

django.setup()

import os
import time
from typing import Any

from homer.bubbles import Concept, Perceptlet
from homer.codelet import Codelet
from homer.coderack import Coderack
from homer.logger import Logger

from runs.models import (
    CodeletRecord,
    CoderackRecord,
    ConceptRecord,
    PerceptletRecord,
    RunRecord,
)


class DjangoLogger(Logger):
    def __init__(self, run: RunRecord, log_directory: str):
        self.run = run
        self.log_directory = log_directory
        self.codelets_run = 0

    @classmethod
    def setup(cls, path_to_logs: str) -> DjangoLogger:
        run_record = RunRecord.objects.create()
        if not os.path.exists(path_to_logs):
            os.makedirs(path_to_logs)
        now = time.localtime()
        year = str(now.tm_year)
        month = str(now.tm_mon)
        day = str(now.tm_mday)
        hour = str(now.tm_hour)
        minute = str(now.tm_min)
        second = str(now.tm_sec)
        date = "-".join(
            [
                value if len(value) >= 2 else "0" + value
                for value in [year, month, day, hour, minute, second]
            ]
        )
        logging_directory = f"{path_to_logs}/{date}"
        os.makedirs(logging_directory)
        return cls(run_record, logging_directory)

    def log(self, item: Any):
        if isinstance(item, str):
            pass
        if isinstance(item, Codelet):
            return self._log_codelet(item)
        if isinstance(item, Coderack):
            return self._log_coderack(item)
        if isinstance(item, Concept):
            return self._log_concept(item)
        if isinstance(item, Perceptlet):
            return self._log_perceptlet(item)

    def log_codelet_run(self, codelet: Codelet):
        codelet_record = CodeletRecord.objects.get(
            codelet_id=codelet.codelet_id, run_id=self.run
        )
        codelet_record.time_run = self.codelets_run
        codelet_record.save()

    def _log_message(self, message):
        print(message)
        messages_file = self.log_directory + "/messages.txt"
        with open(messages_file, "a") as f:
            f.write(message + "\n")

    def _log_codelet(self, codelet: Codelet):
        self._log_message(
            f"    + {codelet.codelet_id} spawned by "
            + f"{codelet.parent_id} - urgency: {codelet.urgency}"
        )
        codelet_record = CodeletRecord.objects.create(
            codelet_id=codelet.codelet_id,
            run_id=self.run,
            codelet_type=type(codelet).__name__,
            birth_time=self.codelets_run,
            urgency=codelet.urgency,
        )
        codelet_record.perceptlet_types.add(
            ConceptRecord.objects.get(
                concept_id=codelet.perceptlet_type.concept_id, run_id=self.run
            )
        )
        if codelet.parent_id == "" or codelet.parent_id[2] == "n":
            return
        codelet_record.parent = CodeletRecord.objects.get(
            codelet_id=codelet.parent_id, run_id=self.run
        )
        codelet_record.save()

    def _log_concept(self, concept: Concept):
        try:
            concept_record = ConceptRecord.objects.get(
                concept_id=concept.concept_id, run_id=self.run
            )
            concept_record.activation.append(
                [self.codelets_run, concept.activation.activation_matrix.tolist()]
            )
            concept_record.save()
        except ConceptRecord.DoesNotExist:
            ConceptRecord.objects.create(
                concept_id=concept.concept_id,
                run_id=self.run,
                name=concept.name,
                activation=[
                    [self.codelets_run, concept.activation.activation_matrix.tolist()]
                ],
            )

    def _log_coderack(self, coderack: Coderack):
        self.codelets_run = coderack.codelets_run
        try:
            coderack_record = CoderackRecord.objects.get(run_id=self.run)
            coderack_record.codelets_run.append(self.codelets_run)
            coderack_record.population.append(len(coderack._codelets))
            coderack_record.save()
        except CoderackRecord.DoesNotExist:
            CoderackRecord.objects.create(
                run_id=self.run,
                codelets_run=[self.codelets_run],
                population=[len(coderack._codelets)],
            )

    def _log_perceptlet(self, perceptlet: Perceptlet):
        self._log_message(
            f"{perceptlet.perceptlet_id} created "
            + f" by {perceptlet.parent_id} - value: {perceptlet.value}; "
            + f"location: {perceptlet.location}; activation: {perceptlet.activation.activation}"
        )
        try:
            perceptlet_record = PerceptletRecord.objects.get(
                run_id=self.run, perceptlet_id=perceptlet.perceptlet_id
            )
            perceptlet_record.activation.append(perceptlet.activation.activation)
            perceptlet_record.unhappiness.append(perceptlet.unhappiness.activation)
            perceptlet_record.quality.append(perceptlet.quality)
            perceptlet_record.save()
        except PerceptletRecord.DoesNotExist:
            perceptlet_record = PerceptletRecord.objects.create(
                perceptlet_id=perceptlet.perceptlet_id,
                run_id=self.run,
                time_created=self.codelets_run,
                value=perceptlet.value,
                location=perceptlet.location,
                activation=[perceptlet.activation.activation],
                unhappiness=[perceptlet.unhappiness.activation],
                quality=[perceptlet.quality],
                parent_codelet=CodeletRecord.objects.get(
                    codelet_id=perceptlet.parent_id, run_id=self.run
                ),
            )
            if hasattr(perceptlet, "parent_concept"):
                perceptlet_record.parent_concept = ConceptRecord.objects.get(
                    concept_id=perceptlet.parent_concept.concept_id, run_id=self.run
                )
                for connection in perceptlet.connections:
                    connection_record = PerceptletRecord.objects.get(
                        perceptlet_id=connection.perceptlet_id, run_id=self.run
                    )
                    perceptlet_record.connections.add(connection_record)
            perceptlet_record.save()

    def graph_concepts(self, concept_names, file_name):
        pass

    def graph_codelets(self, file_name):
        pass

    def graph_coderack(self, file_name):
        pass

    def graph_processes(self, file_name):
        pass

    def graph_codelet_types(self, file_name):
        pass
