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
        elif self.frame == self.view.parent_frame:
            self.satisfaction = self.view.calculate_quality()
            self.view.quality = self.satisfaction
        else:
            if self.frame.has_failed_to_match:
                self.satisfaction = 0
            else:
                total_slots = (
                    len(self.frame.correspondences)
                    + self.frame.number_of_items_left_to_process
                )
                self.satisfaction = (
                    sum(c.quality for c in self.frame.correspondences) / total_slots
                )
