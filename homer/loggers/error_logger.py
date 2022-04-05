from homer.logger import Logger


class ErrorLogger(Logger):
    def __init__(self, error_stream):
        self.error_stream = error_stream

    def log(self, codelet: "Codelet"):
        self.error_stream.write(codelet.codelet_id + "\n")

    def log_message(self, message: str):
        self.error_stream.write(message + "\n")
