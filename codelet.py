from abc import ABC, abstractmethod


class Codelet(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        """Perform main task of the codelet"""
        pass

    @abstractmethod
    def send_activations(self):
        """Send activation(s) to concept node(s)"""
        pass

    @abstractmethod
    def engender_follow_up(self):
        """Place follow-up codelet(s) onto the coderack"""
        pass
