from homer.structures.chunk.slot import Slot


class TemplateSlot(Slot):
    def __init__(self, prototype, form):
        Slot.__init__(self, prototype)
        self.form = form
