import statistics
from typing import Callable, Dict, List, Union

from . import fuzzy
from .classifier import Classifier
from .errors import MissingStructureError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .focus import Focus
from .hyper_parameters import HyperParameters
from .id import ID
from .location import Location
from .logger import Logger
from .problem import Problem
from .random_machine import RandomMachine
from .structure import Structure
from .structure_collection import StructureCollection
from .structures import Frame, LinkOrNode, Space, View
from .structures.links import Correspondence, Label, Relation
from .structures.nodes import Chunk, Concept, Rule
from .structures.nodes.chunks import LetterChunk
from .structures.spaces import ConceptualSpace, ContextualSpace
from .structures.views import SimplexView, MonitoringView
from .worldview import Worldview

# TODO: new_structure methods should accept activation as arg with rand as default


class BubbleChamber:
    def __init__(self):
        self.loggers = {}
        self.random_machine = None
        self.focus = Focus()
        self.worldview = Worldview()

        self.conceptual_spaces = None
        self.contextual_spaces = None
        self.frames = None
        self.frame_instances = None

        self.concepts = None
        self.chunks = None
        self.letter_chunks = None
        self.rules = None

        self.concept_links = None
        self.correspondences = None
        self.labels = None
        self.relations = None

        self.views = None

        self.satisfaction = 0
        self.general_satisfaction = 0
        self.result = None
        self.log_count = 0

        self.ACTIVATION_LOGGING_FREQUENCY = HyperParameters.ACTIVATION_LOGGING_FREQUENCY

    @classmethod
    def setup(cls, loggers: Dict[str, Logger], random_seed: int = None):
        bubble_chamber = cls()
        bubble_chamber.random_machine = RandomMachine(bubble_chamber, random_seed)
        bubble_chamber.reset(loggers)
        return bubble_chamber

    def reset(self, loggers: Dict[str, Logger]):
        self.loggers = loggers
        self.conceptual_spaces = self.new_structure_collection()
        self.contextual_spaces = self.new_structure_collection()
        self.frames = self.new_structure_collection()
        self.frame_instances = self.new_structure_collection()
        self.concepts = self.new_structure_collection()
        self.chunks = self.new_structure_collection()
        self.letter_chunks = self.new_structure_collection()
        self.rules = self.new_structure_collection()
        self.concept_links = self.new_structure_collection()
        self.correspondences = self.new_structure_collection()
        self.labels = self.new_structure_collection()
        self.relations = self.new_structure_collection()
        self.views = self.new_structure_collection()
        self.satisfaction = 0
        self.general_satisfaction = 0
        self.result = None
        self.log_count = 0

    @property
    def spaces(self) -> StructureCollection:
        return StructureCollection.union(
            self.conceptual_spaces, self.contextual_spaces, self.frames
        )

    @property
    def input_spaces(self) -> StructureCollection:
        return StructureCollection.union(
            *[view.input_spaces for view in self.production_views],
            self.contextual_spaces.where(is_main_input=True)
        )

    @property
    def output_spaces(self) -> StructureCollection:
        return self.new_structure_collection(
            *[view.output_space for view in self.production_views]
        )

    @property
    def input_nodes(self) -> StructureCollection:
        return StructureCollection.union(
            *[space.contents.where(is_node=True) for space in self.input_spaces]
        )

    @property
    def labellable_items(self) -> StructureCollection:
        return StructureCollection.union(
            *[space.contents.where(is_labellable=True) for space in self.input_spaces]
        )

    @property
    def comprehension_views(self) -> StructureCollection:
        return self.monitoring_views

    @property
    def production_views(self) -> StructureCollection:
        return StructureCollection.union(self.simplex_views)

    @property
    def monitoring_views(self) -> StructureCollection:
        return self.views.where(is_monitoring_view=True)

    @property
    def discourse_views(self) -> StructureCollection:
        return self.views.where(is_discourse_view=True)

    @property
    def simplex_views(self) -> StructureCollection:
        return self.views.where(is_simplex_view=True)

    @property
    def size_of_raw_input(self) -> int:
        return sum(
            [
                len(space.contents.where(is_raw=True)) * len(space.conceptual_spaces)
                for space in self.contextual_spaces.where(is_main_input=True)
            ]
        )

    @property
    def structures(self) -> StructureCollection:
        return StructureCollection.union(
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
            self.rules,
        )

    def recalculate_satisfaction(self):
        self.focus.recalculate_satisfaction()
        self.recalculate_general_satisfaction()
        if self.focus.view is not None:
            self.satisfaction = max(self.general_satisfaction, self.focus.satisfaction)
        else:
            self.satisfaction = self.general_satisfaction

    def recalculate_general_satisfaction(self):
        spaces = StructureCollection.union(self.input_spaces, self.output_spaces)
        self.general_satisfaction = statistics.fmean(
            [
                statistics.fmean([space.quality for space in spaces]),
                self.worldview.satisfaction,
            ]
        )

    def spread_activations(self):
        for structure in self.structures:
            structure.spread_activation()

    def update_activations(self) -> None:
        for structure in self.structures:
            structure.update_activation()
            if self.log_count % self.ACTIVATION_LOGGING_FREQUENCY == 0:
                self.loggers["structure"].log(structure)
        self.log_count += 1

    def new_structure_collection(
        self, *structures: List[Structure]
    ) -> StructureCollection:
        return StructureCollection(self, structures)

    def add(self, item):
        self.loggers["structure"].log(item)
        for space in item.parent_spaces:
            space.add(item)
            self.loggers["structure"].log(space)
        collections = {
            # views
            MonitoringView: "monitoring_views",
            SimplexView: "simplex_views",
            # spaces
            ConceptualSpace: "conceptual_spaces",
            ContextualSpace: "contextual_spaces",
            Frame: "frames",
            # nodes
            Chunk: "chunks",
            Concept: "concepts",
            LetterChunk: "letter_chunks",
            Rule: "rules",
            # links
            Correspondence: "correspondences",
            Label: "labels",
            Relation: "relations",
        }
        collection_name = collections[type(item)]
        getattr(self, collection_name).add(item)

    def new_conceptual_space(
        self,
        name: str,
        parent_concept: Concept,
        no_of_dimensions: int = 0,
        parent_id: str = "",
        possible_instances: StructureCollection = None,
        dimensions: List[ConceptualSpace] = None,
        sub_spaces: List[ConceptualSpace] = None,
        is_basic_level: bool = False,
        is_symbolic: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
    ) -> ConceptualSpace:
        possible_instances = (
            self.new_structure_collection()
            if possible_instances is None
            else possible_instances
        )
        dimensions = [] if dimensions is None else dimensions
        sub_spaces = [] if sub_spaces is None else sub_spaces
        space = ConceptualSpace(
            structure_id=ID.new(ConceptualSpace),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=self.new_structure_collection(),
            no_of_dimensions=no_of_dimensions,
            dimensions=dimensions,
            sub_spaces=sub_spaces,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
            possible_instances=possible_instances,
            is_basic_level=is_basic_level,
            is_symbolic=is_symbolic,
            super_space_to_coordinate_function_map=super_space_to_coordinate_function_map,
        )
        self.add(space)
        return space

    def new_contextual_space(
        self,
        name: str,
        parent_concept: Concept,
        conceptual_spaces: StructureCollection,
        parent_id: str = "",
        is_main_input: bool = False,
    ) -> ContextualSpace:
        space = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=self.new_structure_collection(),
            conceptual_spaces=conceptual_spaces,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
            is_main_input=is_main_input,
        )
        self.add(space)
        return space

    # TODO: allow frames to be defined as children of other frames with only parts overwritten
    def new_frame(
        self,
        name: str,
        parent_concept: Concept,
        parent_frame: Frame,
        sub_frames: StructureCollection,
        concepts: StructureCollection,
        input_space: ContextualSpace,
        output_space: ContextualSpace,
        parent_id: str = "",
        is_sub_frame: bool = False,
        depth: int = None,
    ) -> Frame:
        frame = Frame(
            structure_id=ID.new(Frame),
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            parent_frame=parent_frame,
            sub_frames=sub_frames,
            concepts=concepts,
            input_space=input_space,
            output_space=output_space,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(),
            instances=self.new_structure_collection(),
            is_sub_frame=is_sub_frame,
            depth=depth,
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
        sub_frames: StructureCollection,
        concepts: StructureCollection,
        input_space: ContextualSpace,
        output_space: ContextualSpace,
        parent_id: str = "",
    ) -> Frame:
        return self.new_frame(
            name,
            parent_concept,
            parent_frame,
            sub_frames,
            concepts,
            input_space,
            output_space,
            parent_id,
            is_sub_frame=True,
        )

    def new_chunk(
        self,
        locations: List[Location],
        parent_space: Space,
        members: StructureCollection = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        left_branch: StructureCollection = None,
        right_branch: StructureCollection = None,
        rule: Rule = None,
        abstract_chunk: Chunk = None,
        is_raw: bool = False,
    ) -> Chunk:
        if members is None:
            members = self.new_structure_collection()
        if left_branch is None:
            left_branch = self.new_structure_collection()
        if right_branch is None:
            right_branch = self.new_structure_collection()
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        chunk = Chunk(
            structure_id=ID.new(Chunk),
            parent_id=parent_id,
            locations=locations,
            members=members,
            parent_space=parent_space,
            quality=quality,
            left_branch=left_branch,
            right_branch=right_branch,
            rule=rule,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            super_chunks=self.new_structure_collection(),
            abstract_chunk=abstract_chunk,
            is_raw=is_raw,
        )
        for member in members:
            member.super_chunks.add(chunk)
            member.recalculate_exigency()
            self.loggers["structure"].log(member)
        self.add(chunk)
        return chunk

    def new_letter_chunk(
        self,
        name: Union[str, None],
        locations: List[Location],
        members: StructureCollection = None,
        parent_space: Space = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
        left_branch: StructureCollection = None,
        right_branch: StructureCollection = None,
        rule: Rule = None,
        meaning_concept: Concept = None,
        grammar_concept: Concept = None,
        abstract_chunk: LetterChunk = None,
    ) -> LetterChunk:
        if left_branch is None:
            left_branch = self.new_structure_collection()
        if right_branch is None:
            right_branch = self.new_structure_collection()
        if members is None:
            members = StructureCollection.union(left_branch, right_branch)
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
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
            rule=rule,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            super_chunks=self.new_structure_collection(),
            abstract_chunk=abstract_chunk,
        )
        for member in members:
            member.super_chunks.add(letter_chunk)
            member.recalculate_exigency()
            self.loggers["structure"].log(member)
        self.add(letter_chunk)
        if meaning_concept is not None:
            self.new_relation(
                parent_id, meaning_concept, letter_chunk, grammar_concept, [], 1.0
            )
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
        depth: int = 1,
        distance_to_proximity_weight: float = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT,
        activation: FloatBetweenOneAndZero = None,
        is_slot: bool = False,
    ) -> Concept:
        locations = [] if locations is None else locations
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
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
            child_spaces=self.new_structure_collection(),
            distance_function=distance_function,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            instances=self.new_structure_collection(),
            depth=depth,
            distance_to_proximity_weight=distance_to_proximity_weight,
            is_slot=is_slot,
        )
        if activation is not None:
            concept._activation = activation
        self.add(concept)
        return concept

    def new_rule(
        self,
        name: str,
        location: Location,
        root_concept: Concept,
        left_concept: Concept,
        right_concept: Concept,
        parent_id: str = "",
        stable_activation: FloatBetweenOneAndZero = None,
    ) -> Rule:
        rule = Rule(
            structure_id=ID.new(Rule),
            parent_id=parent_id,
            name=name,
            location=location,
            root_concept=root_concept,
            left_concept=left_concept,
            right_concept=right_concept,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=self.new_structure_collection(location.space),
            stable_activation=stable_activation,
        )
        self.new_relation(
            parent_id=parent_id,
            start=root_concept,
            end=rule,
            parent_concept=None,
            locations=[],
            quality=1.0,
        )
        self.new_relation(
            parent_id=parent_id,
            start=rule,
            end=left_concept,
            parent_concept=None,
            locations=[],
            quality=1.0,
        )
        if right_concept is not None:
            self.new_relation(
                parent_id=parent_id,
                start=rule,
                end=right_concept,
                parent_concept=None,
                locations=[],
                quality=1.0,
            )
        self.add(rule)
        return rule

    def new_link_or_node(
        self,
        parent_space: Space = None,
        locations: List[Location] = None,
        parent_id: str = "",
        quality: FloatBetweenOneAndZero = 0.0,
    ) -> LinkOrNode:
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        link_or_node = LinkOrNode(
            structure_id=ID.new(LinkOrNode),
            parent_id=parent_id,
            parent_space=parent_space,
            locations=locations,
            quality=quality,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
        )
        for space in parent_spaces:
            space.add(link_or_node)
        self.loggers["structure"].log(link_or_node)
        return link_or_node

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
        is_privileged: bool = False,
    ) -> Correspondence:
        if locations is None:
            if start.parent_space is not None and end.parent_space is not None:
                locations = [
                    start.location_in_space(start.parent_space),
                    end.location_in_space(end.parent_space),
                ]
            else:
                locations = []
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=parent_id,
            start=start,
            end=end,
            arguments=self.new_structure_collection(start, end),
            locations=locations,
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            parent_view=parent_view,
            quality=quality,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            is_privileged=is_privileged,
        )
        if parent_view is not None:
            parent_view.recalculate_exigency()
            parent_view.add(correspondence)
            self.loggers["structure"].log(parent_view)
        start.links_out.add(correspondence)
        start.links_in.add(correspondence)
        start.recalculate_exigency()
        end.links_out.add(correspondence)
        end.links_in.add(correspondence)
        end.recalculate_exigency()
        self.add(correspondence)
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
    ) -> Label:
        parent_space = start.parent_space if parent_space is None else parent_space
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        label = Label(
            structure_id=ID.new(Label),
            parent_id=parent_id,
            start=start,
            arguments=self.new_structure_collection(start),
            parent_concept=parent_concept,
            locations=locations,
            quality=quality,
            parent_space=parent_space,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
        )
        if start is not None:
            start.links_out.add(label)
            start.recalculate_exigency()
            self.loggers["structure"].log(start)
        self.add(label)
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
        activation: FloatBetweenOneAndZero = None,
    ) -> Relation:
        parent_space = start.parent_space if parent_space is None else parent_space
        locations = [] if locations is None else locations
        parent_spaces = self.new_structure_collection(
            *[location.space for location in locations]
        )
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=parent_id,
            start=start,
            end=end,
            arguments=self.new_structure_collection(start, end),
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            locations=locations,
            quality=quality,
            parent_space=parent_space,
            links_in=self.new_structure_collection(),
            links_out=self.new_structure_collection(),
            parent_spaces=parent_spaces,
            is_bidirectional=is_bidirectional,
        )
        if activation is not None:
            relation._activation = activation
        start.links_out.add(relation)
        end.links_in.add(relation)
        start.recalculate_exigency()
        end.recalculate_exigency()
        self.add(relation)
        self.loggers["structure"].log(start)
        self.loggers["structure"].log(end)
        return relation

    def new_simplex_view(self) -> SimplexView:
        raise NotImplementedError

    def new_monitoring_view(self) -> MonitoringView:
        raise NotImplementedError
