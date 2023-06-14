from .float_between_one_and_zero import FloatBetweenOneAndZero
from .structures import View


class Focus:
    def __init__(self):
        self.view = None
        self.frame = None
        self.satisfaction = 0

    @property
    def unhappiness(self):
        return 1 - 0.5 ** self.frame.number_of_items_left_to_process

    def recalculate_satisfaction(self):
        if self.view is None:
            self.satisfaction = 0
        else:
            self.satisfaction = self.view.quality = self.view.calculate_quality()
            for sub_view in self.view.all_sub_views:
                sub_view.quality = sub_view.calculate_quality()
