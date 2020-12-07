import logging
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Union

from ..db import PhasmaConfig


class MultiMap(object):
    """
    Multimap is the underlying data structure for a graph database.
    It allows a single entry to correspond to multiple values.
    """

    def __init__(self, config: PhasmaConfig) -> "MultiMap":
        # Defaultdict with list lets us map multiple values to one key.
        self._multimap: Dict[int, List[int]] = defaultdict(list)

        self.config = config

        if self.config.logging_level:
            self.logger = logging.Logger(__name__)

    def __len__(self) -> int:
        return len(self._multimap)

    def empty(self) -> bool:
        """Checks if the multimap contains no keys.

        Returns:
            bool: True of the map is empty, False otherwise.
        """
        return len(self) == 0

    def contains_key(self, key: int) -> bool:
        """Checks if the multimap has a key.

        Args:
            key (int): The integer-based node-id value

        Returns:
            bool: True if the key is found, False otherwise.
        """
        return key in self._multimap

    def contains_value(self, key: int, value: int) -> bool:
        """Checks if the multimap has a key-value mapping

        Args:
            key (int): The node-id of the key we are checking
            value (int): The node-id of the value we are checking

        Returns:
            bool: True of the value is mapped to the key, False otherwise
        """
        if vals := self.get(key):
            return value in vals

        return False

    def add_edge(self, key: int, value: int) -> bool:
        """Adds an edge between two nodes.

        Args:
            key (int): The key to insert.
            value (int): The value to add to the key's list of values.

        Returns:
            bool: True if the value was added successfully, False otherwise.
        """
        self._multimap[key].append(value)
        return True

    def remove_edge(self, key: int, value: int) -> bool:
        """Removes a relationship between a supplied key and value.

        Args:
            key (int): The key to remove the relationship.
            value (int): The value to remove from the key's list.

        Returns:
            bool: True if edge could be removed, False if it does not exist.
        """
        try:
            self._multimap[key].remove(value)
            return True
        except ValueError as err:
            if self.logger is not None:
                self.logger.warn(err)
            return False

    def remove_key(self, key: int) -> bool:
        """Removes a key from the graph and all relationships

        Args:
            key (int): The node-id to remove.

        Returns:
            bool: True if the key could be removed, False if it does not exist.
        """
        try:
            del self._multimap[key]
            return True
        except KeyError as err:
            if self.logger is not None:
                self.logger.warn(err)
            return False

    def clear_key(self, key: int) -> List[int]:
        """Deletes all values associated with a given key.

        Args:
            key (int): The node to clear.

        Returns:
            List[int]: Returns empty list if no entries,
            the entries otherwise.
        """
        if len(self._multimap[key]) == 0:
            return []

        entries_clone = deepcopy(self._multimap[key])
        self._multimap[key].clear()
        return entries_clone

    def get(self, key: int) -> Union[List[int], None]:
        """Mapped function to underlying dict's "get" operation.

        Args:
            key (int): The node-id to get the list of nodes for.

        Returns:
            Union[List[int], None]: The list of nodes, otherwise None.
        """
        return self._multimap.get(key)

    def clear(self):
        """Clears out the multimap, resetting the length to 0."""
        self._multimap.clear()
