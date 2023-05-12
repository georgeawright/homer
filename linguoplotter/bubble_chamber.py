import math
import statistics
from typing import Callable, Dict, List, Union

from .classifier import Classifier
from .errors import MissingStructureError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .focus import Focus
from .hyper_parameters import HyperParameters
from .id import ID
from .location import Location
from .logger import Logger
from .random_machine import RandomMachine
from .recycle_bin import RecycleBin
from .structure import Structure
from .structure_collections import StructureDict, StructureList, StructureSet
from .structures import Frame, Space, View
from .structures.frames import MergedFrame
from .structures.links import Correspondence, Label, Relation
from .structures.nodes import Chunk, Concept
from .structures.nodes.chunks import LetterChunk
from .structures.nodes.concepts import CompoundConcept
from .structures.spaces import ConceptualSpace, ContextualSpace
from .worldview import Worldview


class BubbleChamber:
    JUMP_THRESHOLD = HyperParameters.JUMP_THRESHOLD
    MAIN_INPUT_WEIGHT = HyperParameters.BUBBLE_CHAMBER_SATISFACTION_MAIN_INPUT_WEIGHT
    VIEWS_WEIGHT = HyperParameters.BUBBLE_CHAMBER_SATISFACTION_VIEW_QUALITIES_WEIGHT
    WORLDVIEW_WEIGHT = HyperParameters.BUBBLE_CHAMBER_SATISFACTION_WORLDVIEW_WEIGHT

    def __init__(self, focus, recycle_bin):
        self.loggers = {}
        self.random_machine = None
        self.worldview = None
        self.focus = focus
        self.recycle_bin = recycle_bin

        self.conceptual_spaces = None
        self.contextual_spaces = None
        self.frames = None
        self.frame_instances = None

        self.concepts = None
        self.chunks = None
        self.letter_chunks = None

        self.concept_links = None
        self.correspondences = None
        self.labels = None
        self.interspatial_labels = None
        self.relations = None
        self.interspatial_relations = None

        self.views = None

        self.satisfaction = 0
        self.general_satisfaction = 0
        self.previous_satisfaction = 0
        self.change_in_satisfaction = 0
        self.focus_setters_since_last_successful_focus_unset = 0
        self.result = None
        self.log_count = 0

        self.ACTIVATION_LOGGING_FREQUENCY = HyperParameters.ACTIVATION_LOGGING_FREQUENCY

    @classmethod
    def setup(cls, loggers: Dict[str, Logger], random_seed: int = None):
        bubble_chamber = cls(Focus(), RecycleBin())
        bubble_chamber.random_machine = RandomMachine(bubble_chamber, random_seed)
        bubble_chamber.reset(loggers)
        return bubble_chamber

    def reset(self, loggers: Dict[str, Logger]):
        self.loggers = loggers
        self.focus = Focus()
        self.worldview = Worldview(None)
        self.conceptual_spaces = self.new_set()
        self.contextual_spaces = self.new_set()
        self.frames = self.new_set()
        self.frame_instances = self.new_set()
        self.concepts = self.new_set()
        self.chunks = self.new_set()
        self.letter_chunks = self.new_set()
        self.concept_links = self.new_set()
        self.correspondences = self.new_set()
        self.labels = self.new_set()
        self.interspatial_labels = self.new_set()
        self.relations = self.new_set()
        self.interspatial_relations = self.new_set()
        self.views = self.new_set()
        self.satisfaction = 0
        self.general_satisfaction = 0
        self.previous_satisfaction = 0
        self.change_in_satisfaction = 0
        self.focus_setters_since_last_successful_focus_unset = 0
        self.result = None
        self.log_count = 0

    @property
    def spaces(self) -> StructureSet:
        return StructureSet.union(
            self.conceptual_spaces, self.contextual_spaces, self.frames
        )

    @property
    def input_spaces(self) -> StructureSet:
        return StructureSet.union(
            *[view.input_spaces for view in self.views],
            self.contextual_spaces.where(is_main_input=True),
        )

    @property
    def output_spaces(self) -> StructureSet:
        return self.new_set(*[view.output_space for view in self.views])

    @property
    def input_nodes(self) -> StructureSet:
        return StructureSet.union(
            *[space.contents.where(is_node=True) for space in self.input_spaces]
        )

    @property
    def size_of_raw_input(self) -> int:
        return sum(
            [
                len(space.contents.where(is_raw=True)) * len(space.conceptual_spaces)
                for space in self.contextual_spaces.where(is_main_input=True)
            ]
        )

    @property
    def structures(self) -> StructureSet:
        return StructureSet.union(
            self.conceptual_spaces,
            self.contextual_spaces,
            self.frames,
            self.chunks,
            self.concepts,
            self.correspondences,
            self.labels,
            self.letter_chunks,
            self.relations,
            self.views,
            self.concept_links,
        )

    @property
    def collections(self) -> dict:
        return {
            # views
            View: "views",
            # spaces
            ConceptualSpace: "conceptual_spaces",
            ContextualSpace: "contextual_spaces",
            Frame: "frames",
            MergedFrame: "merged_frames",
            # nodes
            Chunk: "chunks",
            Concept: "concepts",
            CompoundConcept: "concepts",
            LetterChunk: "letter_chunks",
            # links
            Correspondence: "correspondences",
            Label: "labels",
            Relation: "relations",
        }

    def recalculate_satisfaction(self):
        self.focus.recalculate_satisfaction()
        self.recalculate_general_satisfaction()
        if self.focus.view is not None:
            self.satisfaction = max(self.general_satisfaction, self.focus.satisfaction)
        else:
            self.satisfaction = self.general_satisfaction
        self.change_in_satisfaction = self.satisfaction - self.previous_satisfaction

    def recalculate_general_satisfaction(self):
        main_input_space = self.contextual_spaces.where(is_main_input=True).get()
        average_view_quality = (
            statistics.fmean([view.quality for view in self.views])
            if not self.views.is_empty
            else 0
        )
        self.general_satisfaction = sum(
            [
                self.MAIN_INPUT_WEIGHT * main_input_space.quality,
                self.VIEWS_WEIGHT * average_view_quality,
                self.WORLDVIEW_WEIGHT * self.worldview.satisfaction,
            ]
        )

    def update_activations(self) -> None:
        self.change_in_satisfaction = self.satisfaction - self.previous_satisfaction
        self.previous_satisfaction = self.satisfaction
        self.worldview.activate()
        for structure in self.structures:
            structure.recalculate_activation()
        for structure in self.structures:
            structure.update_activation()
            if (
                structure.activation > self.JUMP_THRESHOLD
                and self.random_machine.coin_flip()
            ):
                structure.activate()
            if self.log_count % self.ACTIVATION_LOGGING_FREQUENCY == 0:
                self.loggers["structure"].log(structure)
        self.log_count += 1

    def new_dict(self, structures: dict = None, name: str = None) -> StructureDict:
        structures = {} if structures is None else structures
        return StructureDict(self, structures, name=name)

    def new_list(self, *structures: list, name: str = None) -> StructureList:
        return StructureList(self, structures, name=name)

    def new_set(self, *structures: list, name: str = None) -> StructureSet:
        return StructureSet(self, structures, name=name)

    def add(self, item):
        self.loggers["structure"].log(item)
        for space in item.parent_spaces:
            space.add(item)
            self.loggers["structure"].log(space)
        collection_name = self.collections[type(item)]
        getattr(self, collection_name).add(item)
        if item.is_interspatial and item.is_label:
            self.interspatial_labels.add(item)
        if item.is_interspatial and item.is_relation:
            self.interspatial_relations.add(item)

    def remove(self, item):
        if item.is_frame:
            self.frames.remove(item)
        if item.is_view:
            item_sub_views = item.sub_views.copy()
            for sub_view in item.sub_views:
                sub_view.super_views.remove(item)
                sub_view.cohesion_views.remove(item)
            for super_view in StructureSet.union(item.super_views, item.cohesion_views):
                for correspondence in super_view.members.copy():
                    if (
                        correspondence.start in item.parent_frame.input_space.contents
                        or correspondence.start
                        in item.parent_frame.output_space.contents
                    ):
                        self.remove(correspondence)
                    if correspondence.parent_view in item_sub_views:
                        super_view.remove(correspondence)
                super_view.sub_views.remove(item)
                for frame in item.frames:
                    super_view.frames.remove(frame)
            correspondences = item.members.where(parent_view=item)
            for correspondence in correspondences:
                self.remove(correspondence)
            item.parent_frame.progenitor.instances.remove(item)
            item.parent_frame.parent_concept.instances.remove(item)
            self.remove(item.parent_frame)
        if item.is_correspondence:
            item.parent_view.remove(item)
        if item.is_link:
            if item.is_interspatial:
                self.interspatial_labels.remove(item)
                self.interspatial_relations.remove(item)
            item.parent_concept.instances.remove(item)
            for argument in item.arguments:
                argument.links_out.remove(item)
                argument.links_in.remove(item)
                argument.champion_labels.remove(item)
                argument.champion_relations.remove(item)
                argument.recalculate_exigency()
        if item.is_relation:
            if item.parent_concept is not None:
                item.parent_concept.instances.remove(item)
            if None not in {item.parent_concept, item.conceptual_space}:
                try:
                    item.parent_concept.relations.where(
                        parent_concept=item.conceptual_space.parent_concept
                    ).get().end.instances.remove(item)
                except MissingStructureError:
                    pass
        if item.is_chunk:
            for view in self.views.copy():
                if item in view.grouped_nodes:
                    self.remove(view)
            for sub_chunk in item.sub_chunks:
                sub_chunk.super_chunks.remove(item)
                sub_chunk.recalculate_exigency()
            for super_chunk in item.super_chunks:
                super_chunk.sub_chunks.remove(item)
            for link in item.links:
                self.remove(link)
        for space in item.parent_spaces:
            space.contents.remove(item)
        if item.is_letter_chunk:
            if item.abstract_chunk is not None:
                item.abstract_chunk.instances.remove(item)
        collection_name = self.collections[type(item)]
        getattr(self, collection_name).remove(item)

    def new_conceptual_space(
        self,
        name: str,
        parent_concept: Concept,
        breadth: int = 1,
        no_of_dimensions: int = 0,
        parent_id: str = "",
        possible_instances: StructureSet = None,
        dimensions: List[ConceptualSpace] = None,
        sub_spaces: List[ConceptualSpace] = None,
        is_basic_level: bool = False,
        is_symbolic: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
    ) -> ConceptualSpace:
        possible_instances = (
            self.new_set() if possible_instances is None else possible_instances
        )
        dimensions = [] if dimensions is None else dimensions
        sub_spaces = [] if sub_spaces is None else sub_spaces
        space = ConceptualSpace(
            structure_id=ID.new(ConceptualSpace),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=self.new_set(),
            breadth=breadth,
            no_of_dimensions=no_of_dimensions,
            dimensions=dimensions,
            sub_spaces=sub_spaces,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=self.new_set(),
            possible_instances=possible_instances,
            is_basic_level=is_basic_level,
            is_symbolic=is_symbolic,
            super_space_to_coordinate_function_map=super_space_to_coordinate_function_map,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        self.add(space)
        return space

    def new_contextual_space(
        self,
        name: str,
        parent_concept: Concept,
        conceptual_spaces: StructureSet,
        parent_id: str = "",
        is_main_input: bool = False,
    ) -> ContextualSpace:
        space = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=self.new_set(),
            conceptual_spaces=conceptual_spaces,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=self.new_set(),
            is_main_input=is_main_input,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        self.add(space)
        return space

    # TODO: allow frames to be defined as children of other frames with only parts overwritten
    def new_frame(
        self,
        name: str,
        parent_concept: Concept,
        parent_frame: Frame,
        sub_frames: StructureSet,
        concepts: StructureSet,
        input_space: ContextualSpace,
        output_space: ContextualSpace,
        interspatial_links: StructureSet = None,
        parent_id: str = "",
        is_sub_frame: bool = False,
        depth: int = None,
    ) -> Frame:
        interspatial_links = (
            self.new_set() if interspatial_links is None else interspatial_links
        )
        frame = Frame(
            structure_id=ID.new(Frame),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            parent_frame=parent_frame,
            sub_frames=sub_frames,
            concepts=concepts,
            interspatial_links=interspatial_links,
            input_space=input_space,
            output_space=output_space,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=self.new_set(),
            instances=self.new_set(),
            is_sub_frame=is_sub_frame,
            depth=depth,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        if parent_frame is not None:
            parent_frame.instances.add(frame)
        self.add(frame)
        return frame

    def new_sub_frame(
        self,
        name: str,
        parent_concept: Concept,
        parent_frame: Frame,
        sub_frames: StructureSet,
        concepts: StructureSet,
        input_space: ContextualSpace,
        output_space: ContextualSpace,
        parent_id: str = "",
    ) -> Frame:
        return self.new_frame(
            name=name,
            parent_concept=parent_concept,
            parent_frame=parent_frame,
            sub_frames=sub_frames,
            concepts=concepts,
            input_space=input_space,
            output_space=output_space,
            parent_id=parent_id,
            is_sub_frame=True,
        )

    def new_merged_frame(
        self,
        name: str,
        parent_concept: "Concept",
        component_frames: StructureList,
        depth: int = None,
        parent_id: str = None,
    ):
        frame = MergedFrame(
            structure_id=ID.new(MergedFrame),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            component_frames=component_frames,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=self.new_set(),
            instances=self.new_set(),
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
            depth=depth,
        )
        self.add(frame)
        return frame

    def new_chunk(
        self,
        locations: List[Location],
        parent_space: Space,
        members: StructureSet = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        activation: FloatBetweenOneAndZero = 0.0,
        abstract_chunk: Chunk = None,
        is_raw: bool = False,
    ) -> Chunk:
        if members is None:
            members = self.new_set()
        locations.append(Location([[len(members)]], self.conceptual_spaces["size"]))
        parent_spaces = self.new_set(*[location.space for location in locations])
        chunk = Chunk(
            structure_id=ID.new(Chunk),
            parent_id=parent_id,
            locations=locations,
            members=members,
            parent_space=parent_space,
            quality=quality,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=parent_spaces,
            instances=self.new_set(),
            super_chunks=self.new_set(),
            sub_chunks=self.new_set(),
            abstract_chunk=abstract_chunk,
            is_raw=is_raw,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        for existing_chunk in self.chunks:
            if not chunk.members.is_empty and all(
                member in existing_chunk.members for member in chunk.members
            ):
                chunk.super_chunks.add(existing_chunk)
                existing_chunk.sub_chunks.add(chunk)
                existing_chunk.recalculate_exigency()
                self.loggers["structure"].log(existing_chunk)
            if not existing_chunk.members.is_empty and all(
                member in chunk.members for member in existing_chunk.members
            ):
                chunk.sub_chunks.add(existing_chunk)
                existing_chunk.super_chunks.add(chunk)
                existing_chunk.recalculate_exigency()
                self.loggers["structure"].log(existing_chunk)
            if existing_chunk.is_raw and existing_chunk in chunk.members:
                existing_chunk.super_chunks.add(chunk)
                chunk.sub_chunks.add(existing_chunk)
                existing_chunk.recalculate_exigency()
                self.loggers["structure"].log(existing_chunk)
        chunk._activation = activation
        self.add(chunk)
        return chunk

    def new_letter_chunk(
        self,
        name: Union[str, None],
        locations: List[Location],
        members: StructureSet = None,
        parent_space: Space = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        left_branch: StructureSet = None,
        right_branch: StructureSet = None,
        meaning_concept: Concept = None,
        grammar_concept: Concept = None,
        abstract_chunk: LetterChunk = None,
    ) -> LetterChunk:
        if left_branch is None:
            left_branch = self.new_set()
        if right_branch is None:
            right_branch = self.new_set()
        if members is None:
            members = StructureSet.union(left_branch, right_branch)
        parent_spaces = self.new_set(*[location.space for location in locations])
        letter_chunk = LetterChunk(
            structure_id=ID.new(LetterChunk),
            parent_id=parent_id,
            name=name,
            locations=locations,
            members=members,
            parent_space=parent_space,
            quality=quality,
            left_branch=left_branch,
            right_branch=right_branch,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=parent_spaces,
            instances=self.new_set(),
            super_chunks=self.new_set(),
            sub_chunks=self.new_set(),
            abstract_chunk=abstract_chunk,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        for member in members:
            member.super_chunks.add(letter_chunk)
            member.recalculate_exigency()
            letter_chunk.sub_chunks.add(member)
            self.loggers["structure"].log(member)
        has_string_location = False
        for location in letter_chunk.locations:
            if location.space == self.conceptual_spaces["string"]:
                location.coordinates = [[letter_chunk.name]]
                has_string_location = True
        if not has_string_location:
            letter_chunk.locations.append(
                Location([[name]], self.conceptual_spaces["string"])
            )
        self.add(letter_chunk)
        if meaning_concept is not None:
            self.new_relation(
                meaning_concept,
                letter_chunk,
                grammar_concept,
                quality=1.0,
                parent_id=parent_id,
            )
        if abstract_chunk is not None:
            abstract_chunk.instances.add(letter_chunk)
        return letter_chunk

    def new_concept(
        self,
        name: str,
        parent_id: str = "",
        locations: List[Location] = None,
        classifier: Classifier = None,
        instance_type: type = None,
        structure_type: type = None,
        parent_space: Space = None,
        distance_function: Callable = None,
        chunking_distance_function: Callable = None,
        possible_instances: StructureSet = None,
        subsumes: StructureSet = None,
        depth: int = 1,
        distance_to_proximity_weight: float = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT,
        activation: FloatBetweenOneAndZero = None,
        is_slot: bool = False,
        reverse: Concept = None,
    ) -> Concept:
        locations = [] if locations is None else locations
        for location in locations:
            for sub_space in location.space.sub_spaces:
                if not any([l.space == sub_space for l in locations]):
                    location_in_sub_space = (
                        sub_space.location_from_super_space_location(location)
                    )
                    locations.append(location_in_sub_space)
        if parent_space is not None:
            if not any([location.space == parent_space for location in locations]):
                locations.append(
                    Location(
                        [[math.nan for _ in range(parent_space.no_of_dimensions)]],
                        parent_space,
                    )
                )
        parent_spaces = self.new_set(*[location.space for location in locations])
        possible_instances = (
            self.new_set() if possible_instances is None else possible_instances
        )
        subsumes = self.new_set() if subsumes is None else subsumes
        chunking_distance_function = (
            chunking_distance_function
            if chunking_distance_function is not None
            else distance_function
        )
        concept = Concept(
            structure_id=ID.new(Concept),
            parent_id=parent_id,
            name=name,
            locations=locations,
            classifier=classifier,
            instance_type=instance_type,
            structure_type=structure_type,
            parent_space=parent_space,
            child_spaces=self.new_set(),
            distance_function=distance_function,
            chunking_distance_function=chunking_distance_function,
            possible_instances=possible_instances,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=parent_spaces,
            instances=self.new_set(),
            subsumes=subsumes,
            depth=depth,
            distance_to_proximity_weight=distance_to_proximity_weight,
            is_slot=is_slot,
            reverse=reverse,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        if activation is not None:
            concept._activation = activation
        self.add(concept)
        return concept

    def new_compound_concept(
        self,
        root: Concept,
        args: List[Concept],
        parent_id: str = "",
        is_slot: bool = False,
        reverse: Concept = None,
        subsumes: StructureSet = None,
    ):
        subsumes = self.new_set() if subsumes is None else subsumes
        try:
            return self.concepts.where(
                is_compound_concept=True, root=root, args=args
            ).get()
        except MissingStructureError:
            parent_spaces = self.new_set(
                *[location.space for location in args[0].locations]
            )
            concept = CompoundConcept(
                structure_id=ID.new(Concept),
                parent_id=parent_id,
                root=root,
                args=args,
                child_spaces=self.new_set(),
                possible_instances=self.new_set(),
                links_in=self.new_set(),
                links_out=self.new_set(),
                parent_spaces=parent_spaces,
                instances=self.new_set(),
                subsumes=subsumes,
                champion_labels=self.new_set(),
                champion_relations=self.new_set(),
                is_slot=is_slot,
                reverse=reverse,
            )
            self.add(concept)
            self.new_relation(root, concept, quality=1.0, parent_id=parent_id)
            for arg in args:
                self.new_relation(arg, concept, quality=1.0, parent_id=parent_id)
            try:
                if all(
                    arg.has_relation_with(
                        self.concepts["more"], parent_concept=self.concepts["more"]
                    )
                    for arg in args
                ):
                    self.new_relation(
                        concept,
                        self.concepts["more"],
                        self.concepts["more"],
                        quality=1.0,
                        parent_id=parent_id,
                    )
                elif all(
                    arg.has_relation_with(
                        self.concepts["less"], parent_concept=self.concepts["more"]
                    )
                    for arg in args
                ):
                    self.new_relation(
                        concept,
                        self.concepts["less"],
                        self.concepts["more"],
                        quality=1.0,
                        parent_id=parent_id,
                    )
            except KeyError:
                pass
            return concept

    def new_correspondence(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        locations: List[Location] = None,
        conceptual_space: ConceptualSpace = None,
        parent_view: View = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        is_excitatory: bool = True,
        is_privileged: bool = False,
        is_projection: bool = False,
    ) -> Correspondence:
        if locations is None:
            if start.parent_space is not None and end.parent_space is not None:
                locations = [
                    start.location_in_space(start.parent_space),
                    end.location_in_space(end.parent_space),
                ]
            else:
                locations = []
        parent_spaces = self.new_set(*[location.space for location in locations])
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=parent_id,
            start=start,
            end=end,
            arguments=self.new_set(start, end),
            locations=locations,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            parent_view=parent_view,
            quality=quality,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=parent_spaces,
            is_excitatory=is_excitatory,
            is_privileged=is_privileged,
            is_projection=is_projection,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        start.links_out.add(correspondence)
        start.links_in.add(correspondence)
        start.recalculate_exigency()
        end.links_out.add(correspondence)
        end.links_in.add(correspondence)
        end.recalculate_exigency()
        self.add(correspondence)
        while parent_view is not None:
            parent_view.add(correspondence)
            parent_view.recalculate_exigency()
            self.loggers["structure"].log(parent_view)
            try:
                parent_view = parent_view.super_views.get()
            except MissingStructureError:
                parent_view = None
        self.loggers["structure"].log(start)
        self.loggers["structure"].log(end)
        return correspondence

    def new_label(
        self,
        start: Structure,
        parent_concept: Concept,
        locations: List[Location],
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        parent_space: ContextualSpace = None,
        is_interspatial: bool = False,
        activation: FloatBetweenOneAndZero = None,
    ) -> Label:
        parent_space = start.parent_space if parent_space is None else parent_space
        parent_spaces = self.new_set(*[location.space for location in locations])
        label = Label(
            structure_id=ID.new(Label),
            parent_id=parent_id,
            start=start,
            arguments=self.new_set(start),
            parent_concept=parent_concept,
            locations=locations,
            quality=quality,
            parent_space=parent_space,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=parent_spaces,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
            is_interspatial=is_interspatial,
        )
        if activation is not None:
            label._activation = activation
        if start is not None:
            start.links_out.add(label)
            start.recalculate_exigency()
            self.loggers["structure"].log(start)
        self.add(label)
        parent_concept.instances.add(label)
        return label

    def new_relation(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept = None,
        locations: List[Location] = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        parent_space: ContextualSpace = None,
        conceptual_space: ConceptualSpace = None,
        is_bidirectional: bool = True,
        is_excitatory: bool = True,
        is_interspatial: bool = False,
        activation: FloatBetweenOneAndZero = None,
        stable_activation: FloatBetweenOneAndZero = None,
    ) -> Relation:
        parent_space = (
            start.parent_space
            if parent_space is None and start.parent_space == end.parent_space
            else parent_space
        )
        locations = [] if locations is None else locations
        parent_spaces = self.new_set(*[location.space for location in locations])
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=parent_id,
            start=start,
            end=end,
            arguments=self.new_set(start, end),
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            locations=locations,
            quality=quality,
            parent_space=parent_space,
            links_in=self.new_set(),
            links_out=self.new_set(),
            parent_spaces=parent_spaces,
            is_bidirectional=is_bidirectional,
            is_excitatory=is_excitatory,
            is_stable=stable_activation is not None,
            is_interspatial=is_interspatial,
            champion_labels=self.new_set(),
            champion_relations=self.new_set(),
        )
        if activation is not None:
            relation._activation = activation
        if stable_activation is not None:
            relation._activation = stable_activation
        start.links_out.add(relation)
        end.links_in.add(relation)
        start.recalculate_exigency()
        end.recalculate_exigency()
        self.add(relation)
        if parent_concept is not None:
            if is_interspatial:
                try:
                    parent_concept.relations.where(
                        parent_concept=self.concepts["outer"]
                    ).get().end.instances.add(relation)
                except MissingStructureError:
                    pass
            else:
                parent_concept.instances.add(relation)
        if None not in {parent_concept, conceptual_space}:
            try:
                concept_to_space_concept = (
                    parent_concept.relations.where(
                        parent_concept=conceptual_space.parent_concept
                    )
                    .get()
                    .end
                )
                if is_interspatial:
                    concept_to_space_concept.relations.where(
                        parent_concept=self.concepts["outer"]
                    ).get().end.instances.add(relation)
                else:
                    concept_to_space_concept.instances.add(relation)
            except MissingStructureError:
                pass
        self.loggers["structure"].log(start)
        self.loggers["structure"].log(end)
        return relation

    def new_view(self) -> View:
        raise NotImplementedError
