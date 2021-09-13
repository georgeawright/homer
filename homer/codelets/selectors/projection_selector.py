from homer.codelets.selector import Selector


class ProjectionSelector(Selector):
    @property
    def _structure_concept(self):
        raise NotImplementedError

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        raise NotImplementedError
