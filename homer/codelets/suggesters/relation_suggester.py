import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError, NoLocationError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import relating_exigency
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace


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
        self.target_space = None
        self.target_structure_one = None
        self.target_structure_two = None
        self.parent_concept = None

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
        print(f"making top down relation suggester for {parent_concept}")
        target_space = StructureCollection(
            {
                space
                for space in bubble_chamber.working_spaces
                if space.no_of_dimensions == 1
                and parent_concept.is_compatible_with(space.parent_concept)
            }
        ).get()
        potential_targets = StructureCollection.union(
            target_space.contents.where(is_chunk=True),
            target_space.contents.where(is_word=True),
        )
        if parent_concept.instance_type == list:
            target_structure_one = potential_targets.get(key=relating_exigency)
            target_structure_two = target_structure_one.get_potential_relative(
                space=target_space, concept=parent_concept
            )
        else:
            try:
                target_structure_one = potential_targets.get(
                    key=lambda x: parent_concept.proximity_to_start(x)
                )
                target_structure_two = potential_targets.get(
                    key=lambda x: parent_concept.proximity_to_end(
                        x, start=target_structure_one.location_in_space(target_space)
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

    def _passes_preliminary_checks(self):
        print(f"suggesting relation {self.codelet_id} spawned by {self.parent_id}")
        self.target_space = self._target_structures["target_space"]
        self.target_structure_one = self._target_structures["target_structure_one"]
        self.target_structure_two = self._target_structures["target_structure_two"]
        self.parent_concept = self._target_structures["parent_concept"]
        print(f"    target space: {self.target_space}")
        print(f"    target structure one: {self.target_structure_one}")
        print(f"    target structure two: {self.target_structure_two}")
        print(f"    parent concept: {self.parent_concept}")
        if self.parent_concept is None:
            try:
                relational_conceptual_spaces = self.bubble_chamber.spaces[
                    "relational concepts"
                ].contents.of_type(ConceptualSpace)
                print(relational_conceptual_spaces)
                compatible_conceptual_spaces = StructureCollection(
                    {
                        space
                        for space in relational_conceptual_spaces
                        if space.is_compatible_with(self.target_space)
                    }
                )
                print(
                    f"    compatible conceptual spaces: {compatible_conceptual_spaces}"
                )
                print(compatible_conceptual_spaces.get().contents)
                self.parent_concept = (
                    compatible_conceptual_spaces.get().contents.of_type(Concept).get()
                )
                print(f"    found parent concept: {self.parent_concept}")
            except MissingStructureError:
                return False
        if self.target_structure_two is None:
            try:
                self.target_structure_two = (
                    self.target_structure_one.get_potential_relative(
                        space=self.target_space, concept=self.parent_concept
                    )
                )
                print(f"    found target structure two: {self.target_structure_two}")
            except MissingStructureError:
                print("    couldn't find second target structure")
                return False
        self._target_structures["target_structure_two"] = self.target_structure_two
        self._target_structures["parent_concept"] = self.parent_concept
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
        print(f"    confidence: {self.confidence}")

    def _fizzle(self):
        pass
