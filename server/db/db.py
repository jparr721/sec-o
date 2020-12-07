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
                default None for no logging.
        """
        self.logging_level = logging_level

    def _generate_config(self) -> PhasmaConfig:
        """Generates a config object from the class members to be passed as
        context to the downstream dependencies of the system.

        Returns:
            PhasmaConfig: The new config object.
        """
        return PhasmaConfig(logging_level=self.logging_level)
