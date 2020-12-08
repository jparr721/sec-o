import logging
from typing import Iterator, List, Union

from ..db import PhasmaConfig
from .multi_map import MultiMap


class ReversibleMultiMap:
    """Reversible multi maps are useful for mapping bidirectionally between
    keys and values in an efficient way. In this context, it's also useful
    for representing edge-weight values in our graph.

    We use "from_to" as the anchor type to base all the other connection
    objects off of. By using integer types we can cheaply keep track of
    references without needing to pass around node-object copies.
    """

    def __init__(self):
        # Connection between two nodes, K->V
        self._from_to = MultiMap(self.config)

        # Edge for "left" node
        self._from_rel = MultiMap(self.config)

        # Connection between two nodes, reversed V->K
        self._to_from = MultiMap(self.config)

        # Edge for "right" node
        self._to_rel = MultiMap(self.config)

    def __len__(self):
        return len(self.from_to)

    def empty(self) -> bool:
        """Checks if the ReversibleMultiMap is empty.

        Returns:
            bool: True if empty, False otherwise.
        """
        return len(self) == 0

    def contains_node(self, node: int) -> bool:
        """Checks if the map contains a node key.

        Args:
            node (int): The integer-based node-id.

        Returns:
            bool: True if the value is present, False otherwise.
        """
        return self._to_from.contains_key(node)

    def contains_entry(self, from_: int, to: int, weight: int) -> bool:
        """Checks to see if a given relationship of weight exists between
        a left and right node in the map. It's important to include the weight
        since two nodes could be related by any arbitrary node value.

        Args:
            from_ (int): The left node being compared.
            to (int): The right node being compared.
            weight (int): The weight between the two nodes.

        Returns:
            bool: True if the relationship exists, False otherwise.
        """
        return self._from_to.contains_value(
            from_, to
        ) and self._from_rel.contains_value(from_, weight)

    def add_edge(self, from_: int, to: int, weight: int) -> bool:
        """Adds a connection between two nodes with a weight node defining
        the relationship.

        Args:
            from_ (int): The left node being added.
            to (int): The right node being added.
            weight (int): The feature defining the relationship.

        Returns:
            bool: True if the relationship was added successfully,
            False otherwise.
        """
        self._from_to.add_edge(from_, to)
        self._from_rel.add_edge(from_, weight)
        self._to_from.add_edge(to, from_)
        return self._to_rel.add_edge(to, weight)

    def remove_edge(self, from_: int, to: int, weight: int) -> bool:
        """Removes a connection between two nodes with a weight node defining
        the relationship.


        Args:
            from_ (int): The left node being removed.
            to (int): The right node being removed.
            weight (int): The feature defining the relationship.

        Returns:
            bool: True if the relationship was removed successfully,
            False otherwise.
        """
        self._from_to.remove_edge(from_, to)
        self._from_rel.remove_edge(from_, weight)
        self._to_from.remove_edge(to, from_)
        return self._to_rel.remove_edge(to, weight)

    def clear_key(self, key: int) -> bool:
        """Clears all entries and relations for a given key.

        Args:
            key (int): The node-id of the key to clear.

        Returns:
            bool: True if the key was cleared, False otherwise.
        """
        removed_edges = self._from_rel.clear_key(key)

        # Short-circuit to avoid useless calculations
        if len(removed_edges) == 0:
            return False

        removed_entries = self._from_to.clear_key(key)

        # Work backwards and clear the V->K entries
        for edge, entry in zip(removed_edges, removed_entries):
            self._to_from.remove_edge(entry, key)
            self._to_rel.remove_edge(entry, edge)

        return True

    def clear(self):
        self._from_to.clear()
        self._from_rel.clear()
        self._to_from.clear()
        self._to_rel.clear()

    def get_nodes_by_key(self, key: int) -> Union[List[int], None]:
        """Returns the list of nodes associated with the left-value
        key of a node pair.

        Args:
            key (int): The node-id to get the list of nodes for.

        Returns:
            Union[List[int], None]: The list of nodes, otherwise None.
        """
        return self._from_to.get(key)

    def get_nodes_by_value(self, key: int) -> Union[List[int], None]:
        """Returns the list of nodes associated with the right-value
        key of a node pair.

        Args:
            key (int): The node-id to get the list of nodes for.

        Returns:
            Union[List[int], None]: The list of nodes, otherwise None.
        """
        return self._to_from.get(key)

    def get_weights_by_key(self, key: int) -> Union[List[int], None]:
        """Returns all the associated weights for a given left-value key in
        a node pair.

        Args:
            key (int): The node-id to get the list of weights for.

        Returns:
            Union[List[int], None]: The list of weights, otherwise None.
        """
        return self._from_rel.get(key)

    def get_weights_by_value(self, key: int) -> Union[List[int], None]:
        """Returns all the associated weights for a given right-value key in
        a node pair.

        Args:
            key (int): The node-id to get the list of weights for.

        Returns:
            Union[List[int], None]: The list of weights, otherwise None.
        """
        return self._to_rel.get(key)

    def get_all_weights(self) -> Union[List[int], None]:
        """Returns all weight values for all keys.

        Returns:
            Union[List[int], None]: The list of values, None if no
            values present.
        """
        return self._from_rel.values()

    def get_all_weights_iter(self) -> Iterator[int]:
        """Returns all weight values as an iterator.

        Yields:
            Iterator[int]: The list of weight node-ids.
        """
        yield self._from_rel.values()

    def get_from_size(self, from_: int) -> int:
        """Returns the number of relations that a left-node has.

        Args:
            from_ (int): The left-node id.

        Returns:
            int: The size of the list of node-ids.
        """
        try:
            return len(self._from_to.get(from_))
        except TypeError as err:
            self.logger.error(err)
            return 0
