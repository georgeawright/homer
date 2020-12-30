from typing import Any, Callable, List

from homer import fuzzy
from .bubble_chamber import BubbleChamber
from .classifier import Classifier
from .coderack import Coderack
from .errors import NoMoreCodelets
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .id import ID
from .location import Location
from .logger import Logger
from .loggers import DjangoLogger
from .problem import Problem
from .structure_collection import StructureCollection
from .structures import Concept
from .structures.links import Relation
from .structures.spaces import ConceptualSpace, WorkingSpace


class Homer:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        logger: Logger,
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.logger = logger
        self.activation_update_frequency = activation_update_frequency

    @classmethod
    def setup(cls, logger: Logger):
        top_level_conceptual_space = ConceptualSpace(
            "top_level_space",
            "",
            "top level",
            None,
            [None],
            StructureCollection(),
            0,
            [],
            [],
        )
        logger.log(top_level_conceptual_space)
        top_level_working_space = top_level_conceptual_space.instance
        logger.log(top_level_working_space)
        bubble_chamber = BubbleChamber(
            StructureCollection({top_level_conceptual_space}),
            StructureCollection({top_level_working_space}),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            StructureCollection(),
            logger,
        )
        bubble_chamber.lexemes = StructureCollection()
        coderack = Coderack.setup(bubble_chamber, logger)
        return cls(bubble_chamber, coderack, logger)

    def run(self):
        while self.bubble_chamber.result is None:
            # time.sleep(1)
            self.logger.log(self.coderack)
            if self.coderack.codelets_run % self.activation_update_frequency == 0:
                self.print_status_update()
                self.bubble_chamber.spread_activations()
                self.bubble_chamber.update_activations()
            try:
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.logger.log("no more codelets")
                self.print_results()
                break
            except Exception as e:
                raise e
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.top_level_working_space.quality,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        bubble_chamber_satisfaction = self.bubble_chamber.satisfaction
        build_activation = self.bubble_chamber.concepts["build"].activation
        evaluate_activation = self.bubble_chamber.concepts["evaluate"].activation
        select_activation = self.bubble_chamber.concepts["select"].activation
        print(
            "================================================================================"
        )
        print(
            f"codelets run: {codelets_run}; "
            + f"satisfaction: {bubble_chamber_satisfaction}; "
            + f"build: {build_activation}; "
            + f"evaluate: {evaluate_activation}; "
            + f"select: {select_activation}; "
        )
        print(
            "================================================================================"
        )
        for chunk in self.bubble_chamber.chunks:
            print(
                chunk.structure_id,
                [space.structure_id for space in chunk.parent_spaces],
            )

    def print_results(self):
        print("results go here")

    def def_concept(
        self,
        name: str = "",
        prototype: Any = None,
        classifier: Classifier = None,
        parent_space: ConceptualSpace = None,
        relevant_value: str = "",
        child_spaces: StructureCollection = None,
        distance_function: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        depth: int = 1,
    ) -> Concept:
        location = (
            Location(prototype, parent_space)
            if prototype is not None
            else Location([], parent_space)
        )
        concept = Concept(
            structure_id=ID.new(Concept),
            parent_id="",
            name=name,
            location=location,
            classifier=classifier,
            relevant_value=relevant_value,
            child_spaces=(
                child_spaces if child_spaces is not None else StructureCollection
            ),
            distance_function=distance_function,
            links_in=links_in,
            links_out=links_out,
            depth=depth,
        )
        parent_space.add(concept)
        self.logger.log(concept)
        self.bubble_chamber.concepts.add(concept)
        return concept

    def def_conceptual_space(
        self,
        name: str = "",
        parent_concept: Concept = None,
        locations: List[Location] = None,
        contents: StructureCollection = None,
        no_of_dimensions: int = 0,
        dimensions: List[ConceptualSpace] = None,
        sub_spaces: List[ConceptualSpace] = None,
        is_basic_level: bool = False,
        coordinates_from_super_space_location: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ) -> ConceptualSpace:
        conceptual_space = ConceptualSpace(
            structure_id=ID.new(ConceptualSpace),
            parent_id="",
            name=name,
            parent_concept=parent_concept,
            locations=(locations if locations is not None else []),
            contents=(contents if contents is not None else StructureCollection()),
            no_of_dimensions=no_of_dimensions,
            dimensions=(dimensions if dimensions is not None else []),
            sub_spaces=(sub_spaces if sub_spaces is not None else []),
            is_basic_level=is_basic_level,
            coordinates_from_super_space_location=coordinates_from_super_space_location,
            links_in=links_in,
            links_out=links_out,
        )
        self.logger.log(conceptual_space)
        for location in locations:
            if location is None:
                continue
            location.space.add(conceptual_space)
        self.bubble_chamber.conceptual_spaces.add(conceptual_space)
        return conceptual_space

    def def_concept_link(
        self, start: Concept, end: Concept, activation: FloatBetweenOneAndZero
    ) -> Relation:
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id="",
            start=start,
            end=end,
            parent_concept=None,
            parent_space=None,
            quality=1.0,
        )
        relation._activation = activation
        start.links_out.add(relation)
        end.links_in.add(relation)
        self.logger.log(relation)
        return relation

    def def_working_space(
        self,
        name: str = "",
        parent_concept: Concept = None,
        locations: List[Location] = None,
        contents: StructureCollection = None,
        no_of_dimensions: int = 0,
        dimensions: List[WorkingSpace] = None,
        sub_spaces: List[WorkingSpace] = None,
        is_basic_level: bool = False,
        coordinates_from_super_space_location: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ) -> WorkingSpace:
        working_space = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id="",
            name=name,
            parent_concept=parent_concept,
            locations=(locations if locations is not None else []),
            contents=(contents if contents is not None else StructureCollection()),
            no_of_dimensions=no_of_dimensions,
            dimensions=(dimensions if dimensions is not None else []),
            sub_spaces=(sub_spaces if sub_spaces is not None else []),
            is_basic_level=is_basic_level,
            coordinates_from_super_space_location=coordinates_from_super_space_location,
            links_in=links_in,
            links_out=links_out,
        )
        self.logger.log(working_space)
        for location in locations:
            if location is None:
                continue
            location.space.add(working_space)
        self.bubble_chamber.working_spaces.add(working_space)
        return working_space
