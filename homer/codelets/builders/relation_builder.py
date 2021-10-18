from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structures.links import Relation


class RelationBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.target_space = None
        self.target_structure_one = None
        self.target_structure_two = None
        self.parent_concept = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import RelationEvaluator

        return RelationEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        self.target_structure_one = self._target_structures["target_structure_one"]
        self.target_structure_two = self._target_structures["target_structure_two"]
        self.target_space = self._target_structures["target_space"]
        self.parent_concept = self._target_structures["parent_concept"]
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _process_structure(self):
        relation = Relation(
            ID.new(Relation),
            self.codelet_id,
            self.target_structure_one,
            self.target_structure_two,
            self.parent_concept,
            self.target_space,
            0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        relation.activation = self.INITIAL_STRUCTURE_ACTIVATION
        self.target_space.add(relation)
        self.target_structure_one.links_out.add(relation)
        self.target_structure_two.links_in.add(relation)
        self.bubble_chamber.relations.add(relation)
        self.bubble_chamber.logger.log(relation)
        self.child_structures = self.bubble_chamber.new_structure_collection(relation)

    def _fizzle(self):
        pass
