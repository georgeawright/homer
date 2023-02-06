from linguoplotter.structures import View


class Worldview:
    def __init__(self, view: View):
        self.view = view
        self.satisfaction = 0

    @property
    def output(self):
        if self.view is None:
            return ""
        return self.view.output

    def activate(self):
        if self.view is None:
            return

        def activate_view(view):
            view.activate()
            for member in view.members:
                member.activate()
            for sub_view in view.sub_views:
                activate_view(sub_view)

        activate_view(self.view)
