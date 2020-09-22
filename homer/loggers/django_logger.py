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
            return ConceptRecord.from_concept(item).save()
        if isinstance(item, Perceptlet):
            return PerceptletRecord.from_perceptlet(item).save()

    def log_codelet_run(self, codelet: Codelet):
        CodeletRecord.objects.get(codelet_id=codelet.codelet_id).update(
            time_run=self.codelets_run
        )

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
        codelet_record.perceptlet_types.set(
            ConceptRecord.objects.get(concept_id=codelet.perceptlet_type.concept_id)
        )
        if codelet.parent_id != "":
            codelet_record.parent = CodeletRecord.objects.get(
                codelet_id=codelet.parent_id
            )
            codelet_record.save()

    def _log_concept(self, concept: Concept):
        ConceptRecord.objects.get(concept_id=concept.concept_id).update(
            activation=concept.activation.activation_matrix
        )

    def _log_coderack(self, coderack: Coderack):
        self.codelets_run = coderack.codelets_run
        coderack_record = CoderackRecord.objects.get(run_id=self.run)
        coderack_record.codelets_run = coderack.codelets_run
        coderack_record.population = len(coderack._codelets)
        coderack_record.save()

    def _log_perceptlet(self, perceptlet: Perceptlet):
        self._log_message(
            f"{perceptlet.perceptlet_id} created "
            + f" by {perceptlet.parent_id} - value: {perceptlet.value}; "
            + f"location: {perceptlet.location}; activation: {perceptlet.activation.activation}"
        )
        perceptlet_record = PerceptletRecord.objects.create(
            perceptlet_id=perceptlet.perceptlet_id,
            run_id=self.run,
            time_created=self.codelets_run,
            value=perceptlet.value,
            location=perceptlet.location,
            activation=perceptlet.activation,
            unhappiness=perceptlet.unhappiness,
            quality=perceptlet.quality,
            parent_concept=ConceptRecord.objects.get(
                concept_id=perceptlet.parent_concept
            ),
            parent_codelet=CodeletRecord.objects.get(
                codelet_id=perceptlet.parent_codelet
            ),
        )
        perceptlet_record.save()
        for connection in perceptlet.connections:
            connection_record = PerceptletRecord.objects.get(
                perceptlet_id=connection.perceptlet_id
            )
            perceptlet_record.connections.add(connection_record)

    def graph_concepts(self, concept_names, file_name):
        pass

    def graph_codelets(self, file_name):
        pass

    def graph_coderack(self, file_name):
        pass

    def graph_processes(self, file_name):
        pass

    def graph_codelet_type(self, file_name):
        pass