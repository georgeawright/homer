from linguoplotter.codelets import Factory


class BottomUpFactory(Factory):
    @property
    def follow_up_urgency(self):
        if self.bubble_chamber.focus.view is None:
            try:
                return max(
                    min(
                        [
                            1 - self.bubble_chamber.satisfaction,
                            self.child_codelets[0].urgency,
                        ]
                    ),
                    self.coderack.MINIMUM_CODELET_URGENCY,
                )
            except IndexError:
                return max(
                    1 - self.bubble_chamber.satisfaction,
                    self.coderack.MINIMUM_CODELET_URGENCY,
                )
        return self.coderack.MINIMUM_CODELET_URGENCY
