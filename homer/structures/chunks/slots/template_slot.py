from homer.location import Location
from homer.word_form import WordForm
from homer.structures import Concept
from homer.structures.chunk.slot import Slot


class TemplateSlot(Slot):
    def __init__(self, prototype: Concept, form: WordForm, location: Location):
        Slot.__init__(self, prototype, location)
        self.form = form
