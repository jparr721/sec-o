from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Union


class MultiMap(object):
    """
    Multimap is the underlying data structure for a graph database.
    It allows a single entry to correspond to multiple values.
    """

    def __init__(self) -> "MultiMap":
        # Defaultdict with list lets us map multiple values to one key.
        self._multimap: Dict[str, List[str]] = defaultdict(list)

    def __len__(self) -> str:
        return len(self._multimap)

    def empty(self) -> bool:
        """Checks if the multimap contains no keys.

        Returns:
            bool: True of the map is empty, False otherwise.
        """
        return len(self) == 0

    def contains_key(self, key: str) -> bool:
        """Checks if the multimap has a key.

        Args:
            key (str): The streger-based node-id value

        Returns:
            bool: True if the key is found, False otherwise.
        """
        return key in self._multimap

    def contains_value(self, key: str, value: str) -> bool:
        """Checks if the multimap has a key-value mapping

        Args:
            key (str): The node-id of the key we are checking
            value (str): The node-id of the value we are checking

        Returns:
            bool: True of the value is mapped to the key, False otherwise
        """
        if vals := self.get(key):
            return value in vals

        return False

    def add_edge(self, key: str, value: str) -> bool:
        """Adds an edge between two nodes.

        Args:
            key (str): The key to insert.
            value (str): The value to add to the key's list of values.

        Returns:
            bool: True if the value was added successfully, False otherwise.
        """
        self._multimap[key].append(value)
        return True

    def remove_edge(self, key: str, value: str) -> bool:
        """Removes a relationship between a supplied key and value.

        Args:
            key (str): The key to remove the relationship.
            value (str): The value to remove from the key's list.

        Returns:
            bool: True if edge could be removed, False if it does not exist.
        """
        try:
            self._multimap[key].remove(value)
            return True
        except ValueError:
            return False

    def remove_key(self, key: str) -> bool:
        """Removes a key from the graph and all relationships

        Args:
            key (str): The node-id to remove.

        Returns:
            bool: True if the key could be removed, False if it does not exist.
        """
        try:
            del self._multimap[key]
            return True
        except KeyError:
            return False

    def clear_key(self, key: str) -> List[str]:
        """Deletes all values associated with a given key.

        Args:
            key (str): The node to clear.

        Returns:
            List[str]: Returns empty list if no entries,
            the entries otherwise.
        """
        if len(self._multimap[key]) == 0:
            return []

        entries_clone = deepcopy(self._multimap[key])
        self._multimap[key].clear()
        return entries_clone

    def get(self, key: str) -> Union[List[str], None]:
        """Mapped function to underlying dict's "get" operation.

        Args:
            key (str): The node-id to get the list of nodes for.

        Returns:
            Union[List[str], None]: The list of nodes, otherwise None.
        """
        return self._multimap.get(key)

    def values(self) -> Union[List[str], None]:
        """Returns all values for all keys.

        Returns:
            Union[List[str], None]: The list of values, None if no
            values present.
        """
        return self._multimap.values()

    def clear(self):
        """Clears out the multimap, resetting the length to 0."""
        self._multimap.clear()
