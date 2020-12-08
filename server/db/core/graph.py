from collections import defaultdict
from typing import Dict, List, Set, Union

from pyroaring import BitMap

from .reversible_multi_map import ReversibleMultiMap


class Graph:
    """The graph structure repsents a traversable, in-memory graph for
    arranging related data by left->edge->[right] connections. It
    features a bi-directional multimap under the hood to make left-hand
    lookups and right-hand lookups very efficient.

    It maintains reference structures to underlying node data to allow for
    the bi-directional multimap to focus on edges, fetching underlying
    data only when absolutely necessary.
    """

    def __init__(self):
        # Counts for each edge (public)
        self.edge_counts: Dict[str, int] = defaultdict(int)

        # Keys for all edges
        self._edge_keys: Dict[int, int] = defaultdict(int)

        # All edges
        self._edges: List[Dict[str, object]] = []

        # All keys for all nodes
        self._node_keys: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(lambda: -1)
        )

        # Nodes mapped by key to the underlying data type
        self._nodes: List[Dict[str, object]] = []

        # Related values
        self._related: Dict[str, ReversibleMultiMap] = defaultdict(
            ReversibleMultiMap
        )

        # Related counts
        self._related_counts: Dict[str, Dict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        # Nodes that are no longer eith us
        self._deleted_nodes = BitMap()

        # Edges that are no longer with us
        self._deleted_edges = BitMap()

    def clear(self):
        """Clears all underlying types, setting their length to 0."""
        self._node_keys.clear()
        self._nodes.clear()
        self._edge_keys.clear()
        self._edges.clear()
        self._related.clear()
        self._edge_counts.clear()
        self._related_counts.clear()
        self._deleted_edges.clear()
        self._deleted_nodes.clear()

    def get_edge_types(self) -> Set[str]:
        """Gets all types of edges that two nodes can have in a set.

        Returns:
            Set[str]: The set of all edge types.
        """
        return set(self._related.keys())

    def get_relationship_type_count(self, type: str) -> Union[int, None]:
        """Gets the number of relationships related to a given type.

        Args:
            type (str): The relationship type to look up.

        Returns:
            Union[int, None]: The number of relationships associated with the
            type, or None if there are no relationships found.
        """
        return self.edge_counts.get(type)

    def get_node_by_key(self, key: str) -> Dict[str, int]:
        """Gets a node by a given key.

        Args:
            key (str): The key to look up.

        Returns:
            Dict[str, int]:
        """
        return self._node_keys.get(key)
