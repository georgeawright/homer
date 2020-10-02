from homer.codelet import Codelet


class FactoryCodelet(Codelet):
    def __init__(self, urgency: float):
        codelet_id = "FactoryCodelet"
        parent_id = ""
        Codelet.__init__(self, urgency, codelet_id, parent_id)

    @classmethod
    def from_components(cls):
        pass

    def run(self) -> Codelet:
        self._select_action()
        self._select_strategy()
        self._select_child_type()
        self._select_target_type()
        return self._spawn_codelet()

    def _select_action(self):
        raise NotImplementedError

    def _select_strategy(self):
        raise NotImplementedError

    def _select_child_type(self):
        raise NotImplementedError

    def _select_target_type(self):
        raise NotImplementedError

    def _spawn_codelet(self) -> Codelet:
        return self.action.codelet_type.from_components(
            self.codelet_id, self.strategy, self.target_type, self.child_type
        )
