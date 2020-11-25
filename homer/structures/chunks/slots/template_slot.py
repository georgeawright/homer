from homer.location import Location
from homer.word_form import WordForm
from homer.structure_collection import StructureCollection
from homer.structures import Concept
from homer.structures.chunks.slot import Slot


class TemplateSlot(Slot):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        prototype: Concept,
        form: WordForm,
        location: Location,
        parent_spaces: StructureCollection,
    ):
        Slot.__init__(
            self,
            structure_id,
            parent_id,
            value=prototype,
            location=location,
            parent_spaces=parent_spaces,
        )
        self.form = form
