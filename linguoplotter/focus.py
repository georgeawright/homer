import statistics

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
            view_items = StructureCollection.union(
                self.view.members, *[member.arguments for member in self.view.members]
            ).filter(lambda x: x.activation > 0)
            if view_items.is_empty():
                self.satisfaction = 0
            else:
                no_of_corresponded_items = len(
                    self.view.parent_frame.corresponded_items
                )
                no_of_items = len(self.view.parent_frame.items)
                self.satisfaction = statistics.fmean(
                    [
                        statistics.fmean([item.quality for item in view_items]),
                        no_of_corresponded_items / no_of_items,
                    ]
                )

    def change_view(self, view: View):
        self.view = view
        self.spaces_quality_history = []
