import statistics

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import View


class Focus:
    def __init__(self):
        self.view = None
        self.spaces_quality_history = []

    @property
    def focussedness(self):
        if self.view is None:
            return 0
        if self.change_in_spaces_quality is None:
            return self.view.unhappiness
        return FloatBetweenOneAndZero(
            self.view.unhappiness + self.change_in_spaces_quality
        )

    @property
    def change_in_spaces_quality(self):
        try:
            return self.spaces_quality_history[-1] - self.spaces_quality_history[-10]
        except IndexError:
            return None

    @property
    def satisfaction(self):
        if self.view is None:
            return 0
        spaces = self.view.input_spaces.copy()
        spaces.add(self.view.output_space)
        return statistics.fmean([space.quality for space in spaces])

    def change_view(self, view: View):
        self.view = view
        self.spaces_quality_history = []
