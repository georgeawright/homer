from .structure_collections import StructureSet


class Worldview:
    def __init__(self, views: StructureSet):
        self.views = views
        self.satisfaction = 0

    @property
    def output(self):
        return ". ".join([view.output for view in self.views])

    def activate(self):
        def activate_view(view):
            view.activate()
            for member in view.members:
                member.activate()
            for sub_view in view.sub_views:
                activate_view(sub_view)

        for view in self.views:
            activate_view(view)
