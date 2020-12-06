from typing import Dict, Any


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

    def generate_config(self) -> Dict[str, Any]:
        return {
            "logging_level": self.logging_level,
        }
