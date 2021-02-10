from __future__ import annotations

import django

django.setup()

import os
import time
from typing import Any

from homer.codelet import Codelet
from homer.codelets import Builder, Evaluator, Selector
from homer.coderack import Coderack
from homer.logger import Logger
from homer.structure import Structure
from homer.tools import last_value_of_dict

from runs.models import (
    CodeletRecord,
    CoderackRecord,
    EventRecord,
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
        codelet_record.result = codelet.result
        codelet_record.save()
        self._log_codelet_events(codelet, codelet_record)

    def _log_message(self, message):
        print(message)
        messages_file = self.log_directory + "/messages.txt"
        with open(messages_file, "a") as f:
            f.write(message + "\n")

    def _log_codelet_events(self, codelet: Codelet, codelet_record):
        event_type = None
        if isinstance(codelet, Builder):
            event_type = "building"
        elif isinstance(codelet, Evaluator):
            event_type = "evaluation"
        elif isinstance(codelet, Selector):
            event_type = "selection"
        if event_type is None:
            return
        target_one = None
        target_two = None
        child_structure = None
        winner = None
        loser = None
        if (
            hasattr(codelet, "target_structure")
            and codelet.target_structure is not None
        ):
            target_one = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.target_structure.structure_id
            )
        if hasattr(codelet, "target_chunk") and codelet.target_chunk is not None:
            target_one = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.target_chunk.structure_id
            )
        if (
            hasattr(codelet, "second_target_structure")
            and codelet.second_target_structure is not None
        ):
            target_two = StructureRecord.objects.get(
                run_id=self.run,
                structure_id=codelet.second_target_structure.structure_id,
            )
        if (
            hasattr(codelet, "second_target_chunk")
            and codelet.second_target_chunk is not None
        ):
            target_two = StructureRecord.objects.get(
                run_id=self.run,
                structure_id=codelet.second_target_chunk.structure_id,
            )
        if hasattr(codelet, "child_structure") and codelet.child_structure is not None:
            child_structure = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.child_structure.structure_id
            )
        if hasattr(codelet, "winner") and codelet.winner is not None:
            winner = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.winner.structure_id
            )
        if hasattr(codelet, "loser") and codelet.loser is not None:
            loser = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.loser.structure_id
            )
        EventRecord.objects.create(
            run_id=self.run,
            event_time=self.codelets_run,
            event_type=event_type,
            codelet=codelet_record,
            target_one=target_one,
            target_two=target_two,
            child_structure=child_structure,
            winner=winner,
            loser=loser,
        )

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
        if (
            hasattr(codelet, "target_structure")
            and codelet.target_structure is not None
        ):
            codelet_record.target_structure = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.target_structure.structure_id
            )
        if (
            hasattr(codelet, "second_target_structure")
            and codelet.second_target_structure is not None
        ):
            codelet_record.second_target_structure = StructureRecord.objects.get(
                run_id=self.run,
                structure_id=codelet.second_target_structure.structure_id,
            )
        if hasattr(codelet, "target_chunk") and codelet.target_chunk is not None:
            codelet_record.target_structure = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.target_chunk.structure_id
            )
        if (
            hasattr(codelet, "second_target_chunk")
            and codelet.second_target_chunk is not None
        ):
            codelet_record.second_target_structure = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.second_target_chunk.structure_id
            )
        if hasattr(codelet, "champion") and codelet.champion is not None:
            codelet_record.champion = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.champion.structure_id
            )
        if hasattr(codelet, "challenger") and codelet.challenger is not None:
            codelet_record.challenger = StructureRecord.objects.get(
                run_id=self.run, structure_id=codelet.challenger.structure_id
            )
        if codelet.parent_id != "coderack":
            codelet_record.parent = CodeletRecord.objects.get(
                codelet_id=codelet.parent_id, run_id=self.run
            )
        codelet_record.save()

    def _log_coderack(self, coderack: Coderack):
        self.codelets_run = coderack.codelets_run
        try:
            coderack_record = CoderackRecord.objects.get(run_id=self.run)
            coderack_record.codelets_run.append(self.codelets_run)
            coderack_record.population.append(len(coderack._codelets))
            coderack_record.satisfaction.append(coderack.bubble_chamber.satisfaction)
            coderack_record.save()
        except CoderackRecord.DoesNotExist:
            CoderackRecord.objects.create(
                run_id=self.run,
                codelets_run=[self.codelets_run],
                population=[len(coderack._codelets)],
                satisfaction=[coderack.bubble_chamber.satisfaction],
            )

    def _log_structure(self, structure: Structure):
        if hasattr(structure, "sub_spaces"):
            for sub_space in structure.sub_spaces:
                self._log_structure(sub_space)
        try:
            structure_record = StructureRecord.objects.get(
                structure_id=structure.structure_id, run_id=self.run
            )
        except StructureRecord.DoesNotExist:
            structure_record = StructureRecord.objects.create(
                structure_id=structure.structure_id,
                run_id=self.run,
                time_created=self.codelets_run,
                value=structure.value,
                locations={},
                activation={},
                unhappiness={},
                quality={},
            )
            self._log_message(
                f"{structure.structure_id} created "
                + f" by {structure.parent_id} - value: {structure.value}; "
                + f"location: {structure.location}; activation: {structure.activation}"
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
            if hasattr(structure, "no_of_dimensions"):
                structure_record.no_of_dimensions = structure.no_of_dimensions
            if hasattr(structure, "is_basic_level"):
                structure_record.is_basic_level = structure.is_basic_level
            if (
                hasattr(structure, "parent_concept")
                and structure.parent_concept is not None
            ):
                structure_record.parent_concept = StructureRecord.objects.get(
                    structure_id=structure.parent_concept.structure_id, run_id=self.run
                )
            if (
                hasattr(structure, "parent_space")
                and structure.parent_space is not None
            ):
                structure_record.parent_space = StructureRecord.objects.get(
                    structure_id=structure.parent_space.structure_id, run_id=self.run
                )

            if hasattr(structure, "start") and structure.start is not None:
                start_record = StructureRecord.objects.get(
                    structure_id=structure.start.structure_id, run_id=self.run
                )
                structure_record.start = start_record
                start_record.links.add(structure_record)
                print(
                    f"{structure.structure_id} linked to {structure.start.structure_id}"
                )
            if hasattr(structure, "end") and structure.end is not None:
                end_record = StructureRecord.objects.get(
                    structure_id=structure.end.structure_id, run_id=self.run
                )
                structure_record.end = end_record
                end_record.links.add(structure_record)
                print(
                    f"{structure.structure_id} linked to {structure.end.structure_id}"
                )
            if hasattr(structure, "dimensions") and structure.dimensions is not None:
                for dimension in structure.dimensions:
                    dimension_record = StructureRecord.objects.get(
                        structure_id=dimension.structure_id, run_id=self.run
                    )
                    structure_record.dimensions.add(dimension_record)
            if hasattr(structure, "sub_spaces") and structure.sub_spaces is not None:
                for sub_space in structure.sub_spaces:
                    sub_space_record = StructureRecord.objects.get(
                        structure_id=sub_space.structure_id, run_id=self.run
                    )
                    structure_record.dimensions.add(sub_space_record)
            if (
                hasattr(structure, "input_spaces")
                and structure.input_spaces is not None
            ):
                for input_space in structure.input_spaces:
                    input_space_record = StructureRecord.objects.get(
                        structure_id=input_space.structure_id, run_id=self.run
                    )
                    structure_record.dimensions.add(input_space_record)
            if (
                hasattr(structure, "output_space")
                and structure.output_space is not None
            ):
                output_space_record = StructureRecord.objects.get(
                    structure_id=structure.output_space.structure_id, run_id=self.run
                )
                structure_record.output_space = output_space_record
            if (
                hasattr(structure, "conceptual_space")
                and structure.conceptual_space is not None
            ):
                conceptual_space_record = StructureRecord.objects.get(
                    structure_id=structure.conceptual_space.structure_id,
                    run_id=self.run,
                )
                structure_record.conceptual_space = conceptual_space_record
        if hasattr(structure, "members") and structure.members is not None:
            for member in structure.members:
                member_record = StructureRecord.objects.get(
                    structure_id=member.structure_id, run_id=self.run
                )
                if member_record in structure_record.members.all():
                    continue
                structure_record.members.add(member_record)
                print(
                    f"{member.structure_id} added as member to {structure.structure_id}"
                )
        if hasattr(structure, "locations") and structure.locations is not None:
            for location in structure.locations:
                if location is None:
                    continue
                space_name = location.space.structure_id
                if space_name not in structure_record.locations:
                    print(f"Adding {structure.structure_id} to {space_name}")
                structure_record.locations[space_name] = location.coordinates
                space_record = StructureRecord.objects.get(
                    structure_id=space_name, run_id=self.run
                )
                space_record.contents.add(structure_record)
        elif hasattr(structure, "location") and structure.location is not None:
            space_name = location.space.structure_id
            if space_name not in structure_record.locations:
                print(f"Adding {structure.structure_id} to {space_name}")
            structure_record.locations[space_name] = location.coordinates
            space_record = StructureRecord.objects.get(
                structure_id=space_name, run_id=self.run
            )
            space_record.contents.add(structure_record)
        structure_record.activation[self.codelets_run] = structure.activation
        structure_record.unhappiness[self.codelets_run] = structure.unhappiness
        structure_record.quality[self.codelets_run] = structure.quality
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
