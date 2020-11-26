from __future__ import annotations

import django

django.setup()

import os
import time
from typing import Any

from homer.codelet import Codelet
from homer.coderack import Coderack
from homer.logger import Logger
from homer.structure import Structure

from runs.models import (
    CodeletRecord,
    CoderackRecord,
    ConceptRecord,
    StructureRecord,
    StructureUpdateRecord,
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
        if isinstance(item, Structure):
            return self._log_structure(item)

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
            target_structure=None
            if codelet.target_structure is None
            else StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.target_structure.structure_id
            ),
        )
        if codelet.parent_id == "coderack":
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

    def _log_structure(self, structure: Structure):
        self._log_message(
            f"{structure.structure_id} created "
            + f" by {structure.parent_id} - value: {structure.value}; "
            + f"location: {structure.location.coordinates}, {structure.location.space.name}; activation: {structure.activation}"
        )
        structure_record = StructureRecord.objects.create(
            structure_id=structure.structure_id,
            run_id=self.run,
            time_created=self.codelets_run,
            value=structure.value,
            location=structure.location.coordinates,
            activation=[structure.activation],
            unhappiness=[structure.unhappiness],
            quality=[structure.quality],
        )
        if structure.parent_id != "":
            parent_codelet = CodeletRecord.objects.get(
                codelet_id=structure.parent_id, run_id=self.run
            )
            structure_record.parent_codelet = parent_codelet
            StructureUpdateRecord.objects.create(
                run_id=self.run,
                time=self.codelets_run,
                codelet_id=parent_codelet.id,
                structure_id=structure_record.id,
                action="Created",
            )
        if hasattr(structure, "parent_concept"):
            structure_record.parent_concept = ConceptRecord.objects.get(
                concept_id=structure.parent_concept.structure_id, run_id=self.run
            )
        if hasattr(structure, "first_argument"):
            structure_record.first_argument = structure.first_argument.structure_id
        if hasattr(structure, "second_argument"):
            structure_record.second_argument = structure.second_argument.structure_id
        for connection in structure.connections:
            connection_record = StructureRecord.objects.get(
                structure_id=connection.structure_id, run_id=self.run
            )
            structure_record.connections.add(connection_record)
        structure_record.save()

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
