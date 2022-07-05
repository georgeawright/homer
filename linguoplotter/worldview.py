from .structure_collection import StructureCollection


class Worldview:
    def __init__(self, views: StructureCollection):
        self.views = views
        self.satisfaction = 0

    @property
    def output(self):
        return ". ".join([view.output for view in self.views])
