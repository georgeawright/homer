from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation, exigency, unhappiness


class StructureConceptDrivenFactory(Factory):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)
        self.structure_collection_key = lambda x: 0

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = 1 - self.bubble_chamber.satisfaction
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY

    def _engender_follow_up(self):
        follow_up_class = self._decide_follow_up_class()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Follow-up class: {follow_up_class.__name__}"
        )
        follow_up = follow_up_class.make(self.codelet_id, self.bubble_chamber)
        self.child_codelets.append(follow_up)

    def _decide_follow_up_class(self):
        follow_up_theme = self.bubble_chamber.random_machine.select(
            self.codelet_themes().values()
        )
        return self._get_codelet_type_from_concepts(
            action=follow_up_theme["actions"].get(key=self.structure_collection_key),
            space=follow_up_theme["spaces"].get(key=self.structure_collection_key),
            direction=follow_up_theme["directions"].get(
                key=self.structure_collection_key
            ),
            structure=follow_up_theme["structures"].get(
                key=self.structure_collection_key
            ),
        )


class RandomStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, urgency
        )


class ActiveStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, urgency
        )
        self.structure_collection_key = activation


class ExigentStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, urgency
        )
        self.structure_collection_key = exigency


class UnhappyStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, urgency
        )
        self.structure_collection_key = unhappiness
