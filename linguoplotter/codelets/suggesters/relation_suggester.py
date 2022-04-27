import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import relating_exigency
from linguoplotter.structures.links import Relation
from linguoplotter.structures.nodes import Concept


class RelationSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_space = target_structures.get("target_space")
        self.target_structure_one = target_structures.get("target_structure_one")
        self.target_structure_two = target_structures.get("target_structure_two")
        self.parent_concept = target_structures.get("parent_concept")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import RelationBuilder

        return RelationBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["parent_concept"] is not None else "BottomUp"
        )
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        target = input_space.contents.where(is_chunk=True, is_slot=False).get(
            key=relating_exigency
        )
        target_space = target.parent_spaces.where(
            is_conceptual_space=True, no_of_dimensions=1
        ).get()
        urgency = urgency if urgency is not None else target.unrelatedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_space": target_space,
                "target_structure_one": target,
                "target_structure_two": None,
                "parent_concept": None,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        conceptual_space = input_space.conceptual_spaces.where(no_of_dimensions=1).get()
        potential_targets = input_space.contents.where(is_node=True, is_slot=False)
        try:
            target_structure_one, target_structure_two = potential_targets.pairs.get(
                key=lambda x: parent_concept.classifier.classify(
                    start=x[0], end=x[1], space=conceptual_space
                )
            )
        except NoLocationError:
            raise MissingStructureError
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean(
                [target_structure_one.unrelatedness, target_structure_two.unrelatedness]
            )
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_space": conceptual_space,
                "target_structure_one": target_structure_one,
                "target_structure_two": target_structure_two,
                "parent_concept": parent_concept,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    @property
    def targets_dict(self):
        return {
            "target_space": self.target_space,
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
            "parent_concept": self.parent_concept,
        }

    def _passes_preliminary_checks(self):
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.conceptual_spaces.where(structure_type=Relation)
                .get()
                .contents.where(is_concept=True, is_slot=False)
                .get()
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found parent concept: {self.parent_concept}"
            )
        if self.target_structure_two is None:
            try:
                self.target_structure_two = (
                    self.target_structure_one.get_potential_relative(
                        space=self.target_space, concept=self.parent_concept
                    )
                )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target structure two: {self.target_structure_two}"
                )
            except MissingStructureError:
                return False
        return self.target_structure_one.relations.where(
            conceptual_space=self.target_space,
            parent_concept=self.parent_concept,
            start=self.target_structure_one,
            end=self.target_structure_two,
        ).is_empty()

    def _calculate_confidence(self):
        self.confidence = (
            self.parent_concept.classifier.classify(
                concept=self.parent_concept,
                space=self.target_space,
                start=self.target_structure_one,
                end=self.target_structure_two,
            )
            * min(self.target_structure_one.quality, self.target_structure_two.quality)
        )

    def _fizzle(self):
        pass