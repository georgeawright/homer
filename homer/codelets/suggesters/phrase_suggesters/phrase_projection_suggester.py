from homer.bubble_chamber import BubbleChamber
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.codelets.suggesters import PhraseSuggester
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation
from homer.structures.views import DiscourseView


class PhraseProjectionSuggester(PhraseSuggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        PhraseSuggester.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )
        self.target_correspondence = None
        self.target_view = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.phrase_builders import PhraseProjectionBuilder

        return PhraseProjectionBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
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

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: DiscourseView = None,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = (
            bubble_chamber.discourse_views.get(key=activation)
            if target_view is None
            else target_view
        )
        frame = target_view.input_frames.get()
        target_correspondence = StructureCollection(
            {
                member
                for member in target_view.members
                if member.start_space != frame
                and member.end_space != target_view.output_space
            }
        ).get(key=activation)
        urgency = (
            urgency
            if urgency is not None
            else target_correspondence.start.uncorrespondedness
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_correspondence": target_correspondence},
            urgency,
        )

    def _passes_preliminary_checks(self) -> bool:
        self.target_correspondence = self._target_structures["target_correspondence"]
        self.target_view = self.target_correspondence.parent_view
        return not self.target_correspondence.start.has_correspondence_to_space(
            self.target_view.output_space
        )

    def _calculate_confidence(self):
        self.confidence = self.target_correspondence.activation

    def _fizzle(self):
        pass
