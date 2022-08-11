import statistics

from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ViewEvaluator


class SimplexViewEvaluator(ViewEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.simplex_views.get(
            key=lambda x: abs(x.activation - x.quality)
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            abs(target.activation - target.quality),
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.view_selectors import SimplexViewSelector

        return SimplexViewSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view-simplex"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_view = self.target_structures.get()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found target view: {target_view}"
        )
        average_correspondence_quality = (
            statistics.fmean(
                [
                    member.quality
                    for member in target_view.members
                    if member.start.parent_space.is_main_input
                ]
            )
            if len(
                target_view.members.filter(lambda x: x.start.parent_space.is_main_input)
            )
            > 0
            else 0
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Average correspondence quality: {average_correspondence_quality}"
        )
        frame = target_view.parent_frame
        proportion_of_frame_output_items_projected = sum(
            1
            for item in frame.output_space.contents.where(is_correspondence=False)
            if item.has_correspondence_to_space(target_view.output_space)
        ) / sum(
            1 for item in frame.output_space.contents.where(is_correspondence=False)
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            "Proportion of frame output items projected: "
            + f"{proportion_of_frame_output_items_projected}",
        )
        try:
            input_chunks_quality = min(
                [
                    chunk.quality
                    for chunk in target_view.grouped_nodes
                    if chunk.parent_space in target_view.input_spaces
                ]
            )
        except ValueError:
            input_chunks_quality = 1
        self.confidence = (
            fuzzy.AND(
                average_correspondence_quality,
                proportion_of_frame_output_items_projected,
            )
            * input_chunks_quality
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_view.activation
