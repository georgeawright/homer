from homer.codelet import Codelet


class FactoryCodelet(Codelet):
    def __init__(self, urgency: float):
        codelet_id = "FactoryCodelet"
        parent_id = ""
        Codelet.__init__(urgency, codelet_id, parent_id)

    def run(self) -> Codelet:
        self._select_action()
        self._select_direction()
        self._select_child_type()
        self._select_target_type()
        return self._spawn_codelet()

    def _select_action(self):
        pass

    def _select_direction(self):
        pass

    def _select_child_type(self):
        pass

    def _select_target_type(self):
        pass

    def _spawn_codelet(self) -> Codelet:
        pass
