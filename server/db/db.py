from collections import namedtuple

PhasmaConfig = namedtuple("PhasmaConfig", ["logging_level"])


class PhasmaDB:
    """PhasmaDB represents the top-level database object to be used
    at runtime.
    """

    def __init__(self, logging_level: str = None):
        """
        Args:
            logging_level (str): The logging level to use,
                default None for no logging
        """
        self.logging_level = logging_level

    def __call__(self):
        """The call override makes the PhasmaDB instance callable to
        start up the embedded database operation.
        """
        pass

    def generate_config(self) -> PhasmaConfig:
        return PhasmaConfig(logging_level=self.logging_level)
