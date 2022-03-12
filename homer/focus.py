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

    @property
    def satisfaction(self):
        if self.view is None:
            return 0
        view_items = StructureCollection.union(
            self.view.members, *[member.arguments for member in self.view.members]
        ).filter(lambda x: x.activation > 0)
        if view_items.is_empty():
            return 0
        return statistics.fmean([item.quality for item in view_items])
        # spaces = self.view.input_spaces.copy()
        # spaces.add(self.view.output_space)
        # return statistics.fmean([space.quality for space in spaces])

    def change_view(self, view: View):
        self.view = view
        self.spaces_quality_history = []
