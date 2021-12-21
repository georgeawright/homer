import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError, NoLocationError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import relating_exigency
from homer.structures.links import Relation
from homer.structures.nodes import Concept


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
        from homer.codelets.builders import RelationBuilder

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
        target_space = bubble_chamber.working_spaces.where(no_of_dimensions=1).get()
        potential_targets = StructureCollection.union(
            target_space.contents.where(is_chunk=True),
            target_space.contents.where(is_word=True),
        )
        target = potential_targets.get(key=relating_exigency)
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
        target_space = bubble_chamber.new_structure_collection(
            space
            for space in bubble_chamber.contextual_spaces
            if space.no_of_dimensions == 1
            and parent_concept.is_compatible_with(space.parent_concept)
        ).get()
        potential_targets = StructureCollection.union(
            target_space.contents.where(is_chunk=True),
            target_space.contents.where(is_word=True),
        )
        try:
            target_structure_one = potential_targets.get(
                key=lambda x: parent_concept.proximity_to_start(x),
            )
            target_structure_two = target_structure_one.get_potential_relative(
                space=target_space, concept=parent_concept
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
                "target_space": target_space,
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
            conceptual_space = (
                self.bubble_chamber.conceptual_spaces.where(
                    is_basic_level=True, instance_type=type(self.target_structure_one)
                )
                .filter(lambda x: self.target_structure_one.has_location_in_space(x))
                .get()
            )
            location = self.target_structure_one.location_in_space(conceptual_space)
            try:
                self.parent_concept = (
                    conceptual_space.contents.where(
                        is_concept=True, structure_type=Relation
                    )
                    .filter(
                        lambda x: any(
                            [
                                location.start_is_near(location)
                                for location in x.locations
                                if location.space == conceptual_space
                            ]
                        )
                    )
                    .get()
                )
            except MissingStructureError:
                try:
                    self.parent_concept = (
                        conceptual_space.contents.where(
                            is_concept=True, structure_type=Relation
                        )
                        .where_not(classifier=None)
                        .get()
                    )
                except MissingStructureError:
                    return False
        if self.target_structure_two is None:
            try:
                self.target_structure_two = (
                    self.target_structure_one.get_potential_relative(
                        space=self.target_space, concept=self.parent_concept
                    )
                )
            except MissingStructureError:
                return False
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept,
            space=self.target_space,
            start=self.target_structure_one,
            end=self.target_structure_two,
        )

    def _fizzle(self):
        pass
