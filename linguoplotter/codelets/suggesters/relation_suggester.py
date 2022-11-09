import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structure_collection_keys import relating_exigency
from linguoplotter.structures.links import Relation
from linguoplotter.structures.nodes import Concept


class RelationSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, targets, urgency
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import RelationBuilder

        return RelationBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = "TopDown" if targets["concept"] is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        start = input_space.contents.filter(
            lambda x: x.is_chunk and not x.is_slot and x.quality > 0
        ).get(key=relating_exigency)
        # TODO:
        # what about same/different location?
        # get all structures at once as in view driven factory
        # probably first get start and end here and concept and space in prelim checks
        target_space = start.parent_spaces.where(
            is_conceptual_space=True, no_of_dimensions=1
        ).get()
        urgency = urgency if urgency is not None else start.unrelatedness
        targets = bubble_chamber.new_dict(
            {"start": start, "space": target_space}, name="targets"
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        input_space = bubble_chamber.input_spaces.get()
        target_space = input_space.conceptual_spaces.where(no_of_dimensions=1).get()
        potential_targets = input_space.contents.filter(
            lambda x: x.is_node and x.is_slot and x.quality > 0
        )
        try:
            possible_pairs = [
                (a, b) for a in potential_targets for b in potential_targets if a != b
            ]
            start, end = bubble_chamber.random_machine.select(
                possible_pairs,
                key=lambda x: parent_concept.classifier.classify(
                    start=x[0], end=x[1], space=target_space
                ),
            )

        except NoLocationError:
            raise MissingStructureError
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([start.unrelatedness, end.unrelatedness])
        )
        targets = bubble_chamber.new_dict(
            {
                "start": start,
                "end": end,
                "space": target_space,
                "concept": parent_concept,
            },
            name="targets",
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if self.targets["concept"] is not None:
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=self.targets["space"],
                start=self.targets["start"],
                end=self.targets["end"],
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < 0.5:
                self.targets["concept"] = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.targets["concept"]]
                )
            if self.targets["end"] is None:
                try:
                    self.targets["end"] = self.targets["start"].get_potential_relative(
                        space=self.targets["space"], concept=self.targets["concept"]
                    )
                except MissingStructureError:
                    return False
        else:
            if self.targets["end"] is None:
                try:
                    self.targets["end"] = (
                        self.targets["start"]
                        .parent_space.contents.filter(
                            lambda x: x != self.targets["start"]
                            and x.is_chunk
                            and x.quality > 0
                        )
                        .get(key=relating_exigency)
                    )
                except MissingStructureError:
                    return False
            self.targets["concept"] = (
                self.bubble_chamber.concepts.where(
                    structure_type=Relation, is_slot=False
                )
                .where_not(classifier=None)
                .filter(
                    lambda x: self.targets["start"]
                    .relations.where(
                        parent_concept=x,
                        conceptual_space=self.targets["space"],
                        end=self.targets["end"],
                    )
                    .is_empty
                )
                .get(
                    key=lambda x: x.classifier.classify(
                        concept=x,
                        space=self.targets["space"],
                        start=self.targets["start"],
                        end=self.targets["end"],
                    )
                )
            )
        return True

    def _calculate_confidence(self):
        classification = self.targets["concept"].classifier.classify(
            concept=self.targets["concept"],
            space=self.targets["space"],
            start=self.targets["start"],
            end=self.targets["end"],
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = (
            classification
            * min(self.targets["start"].quality, self.targets["end"].quality)
            / self.targets["concept"].number_of_components
        )

    def _fizzle(self):
        pass
