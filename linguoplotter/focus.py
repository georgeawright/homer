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
            members = self.view.members.filter(
                lambda x: any(
                    [
                        x.start in self.frame.input_space.contents,
                        x.start in self.frame.output_space.contents,
                        x.end in self.frame.input_space.contents,
                        x.end in self.frame.output_space.contents,
                    ]
                )
            )
            if any(
                [
                    member.parent_concept.is_compound_concept
                    and member.parent_concept.root.name == "not"
                    for member in members
                ]
            ):
                self.satisfaction = 0
            else:
                total_slots = len(members) + self.frame.number_of_items_left_to_process
                self.satisfaction = (
                    sum(member.quality for member in members) / total_slots
                )
