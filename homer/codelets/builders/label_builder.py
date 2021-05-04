from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.structures.links import Label
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace
from homer.tools import project_item_into_space


class LabelBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_node: Node,
        urgency: FloatBetweenOneAndZero,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_node = target_node
        self.parent_concept = parent_concept

    @classmethod
    def get_target_class(cls):
        return Label

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_node: Node,
        urgency: FloatBetweenOneAndZero,
        parent_concept: Concept = None,
    ):
        qualifier = "TopDown" if parent_concept is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_node,
            urgency,
            parent_concept,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target = bubble_chamber.input_nodes.get_unhappy()
        urgency = urgency if urgency is not None else target.unlinkedness
        return cls.spawn(parent_id, bubble_chamber, target, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target = StructureCollection(
            {
                node
                for node in bubble_chamber.input_nodes
                if isinstance(node.value, parent_concept.instance_type)
            }
        ).get_unhappy()
        urgency = urgency if urgency is not None else target.unlinkedness
        return cls.spawn(
            parent_id, bubble_chamber, target, urgency, parent_concept=parent_concept
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.spaces["label concepts"]
                .contents.of_type(ConceptualSpace)
                .where(is_basic_level=True)
                .where(instance_type=type(self.target_node.value))
                .get_random()
                .contents.of_type(Concept)
                .where_not(classifier=None)
                .get_random()
            )
        return not self.target_node.has_label(self.parent_concept)

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept, start=self.target_node
        )

    def _process_structure(self):
        space = self.parent_concept.parent_space.instance_in_space(
            self.target_node.parent_space
        )
        self.bubble_chamber.logger.log(space)
        if self.target_node not in space.contents:
            project_item_into_space(self.target_node, space)
        label = Label(
            ID.new(Label),
            self.codelet_id,
            self.target_node,
            self.parent_concept,
            space,
            0,
        )
        label.activation = self.INITIAL_STRUCTURE_ACTIVATION
        space.add(label)
        self.target_node.links_out.add(label)
        self.bubble_chamber.labels.add(label)
        self.bubble_chamber.working_spaces.add(space)
        top_level_working_space = self.bubble_chamber.spaces["top level working"]
        space.locations.append(Location([], top_level_working_space))
        top_level_working_space.add(space)
        space.parent_spaces.add(self.bubble_chamber.spaces["top level working"])
        self.bubble_chamber.logger.log(label)
        self.child_structures = StructureCollection({label})

    def _fizzle(self):
        self._re_engender()

    def _fail(self):
        self._re_engender()

    def _re_engender(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )
