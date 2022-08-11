import statistics

from linguoplotter import fuzzy
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .structure_collection import StructureCollection
from .structures import View


class Focus:
    def __init__(self):
        self.view = None
        self.spaces_quality_history = []
        self.satisfaction = 0

    @property
    def focussedness(self):
        if self.view is None:
            return 0
        if self.change_in_spaces_quality is None:
            return self.view.unhappiness
        return FloatBetweenOneAndZero(
            self.view.unhappiness
            + self.change_in_spaces_quality * len(self.spaces_quality_history)
        )

    @property
    def change_in_spaces_quality(self):
        try:
            difference = (
                self.spaces_quality_history[-1] - self.spaces_quality_history[0]
            )
            diff_float = (
                0.5 / difference
                if difference > 0
                else -1 * (1 - (0.5 / difference))
                if difference < 0
                else 0
            )
            return 0.5 + diff_float
        except IndexError:
            return None

    def recalculate_satisfaction(self):
        if self.view is None:
            self.satisfaction = 0
        else:
            average_correspondence_quality = (
                statistics.fmean(
                    [
                        member.quality
                        for member in self.view.members
                        if member.start.parent_space.is_main_input
                    ]
                )
                if len(
                    self.view.members.filter(
                        lambda x: x.start.parent_space.is_main_input
                    )
                )
                > 0
                else 0
            )
            frame = self.view.parent_frame
            proportion_of_frame_output_items_projected = sum(
                1
                for item in frame.output_space.contents.where(is_correspondence=False)
                if item.has_correspondence_to_space(self.view.output_space)
            ) / sum(
                1 for item in frame.output_space.contents.where(is_correspondence=False)
            )
            try:
                input_chunks_quality = min(
                    [
                        chunk.quality
                        for chunk in self.view.grouped_nodes
                        if chunk.parent_space in self.view.input_spaces
                    ]
                )
            except ValueError:
                input_chunks_quality = 1
            self.satisfaction = (
                fuzzy.AND(
                    average_correspondence_quality,
                    proportion_of_frame_output_items_projected,
                )
                * input_chunks_quality
            )
            self.view.quality = self.satisfaction

    def change_view(self, view: View):
        self.view = view
        self.spaces_quality_history = []
