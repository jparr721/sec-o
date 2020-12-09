from collections import defaultdict
from typing import Dict, Set, Union, List
from uuid import uuid4

from .reversible_multi_map import ReversibleMultiMap


class Graph:
    """The graph structure repsents a traversable, in-memory graph for
    arranging related data by left->edge->[right] connections. It
    features a bi-directional multimap under the hood to make left-hand
    lookups and right-hand lookups very efficient.

    It mastrains reference structures to underlying node data to allow for
    the bi-directional multimap to focus on edges, fetching underlying
    data only when absolutely necessary.
    """

    def __init__(self):
        # Counts for each edge (public)
        self.edge_counts: Dict[str, int] = defaultdict(int)

        # Keys for all edges
        self._edge_keys: Dict[str, Dict[str, str]] = defaultdict(
            lambda: defaultdict(str)
        )

        # All edges
        self._edges: Dict[str, object] = {}

        # All keys for all nodes
        self._node_keys: Dict[str, Dict[str, str]] = defaultdict(
            lambda: defaultdict(lambda: -1)
        )

        # Nodes mapped by key to the underlying data type
        self._nodes: Dict[str, object] = {}

        # Related values
        self._related: Dict[str, ReversibleMultiMap] = defaultdict(
            ReversibleMultiMap
        )

        # Related counts
        self._related_counts: Dict[str, Dict[str, str]] = defaultdict(
            lambda: defaultdict(str)
        )

        # Nodes that are no longer eith us
        self._deleted_nodes: List[str] = []

        # Edges that are no longer with us
        self._deleted_edges: List[str] = []

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

    def get_edge_type_count(self, type: str) -> Union[str, None]:
        """Gets the number of edges related to a given type.

        Args:
            type (str): The edge type to look up.

        Returns:
            Union[str, None]: The number of edges associated with the
            type, or None if there are no edges found.
        """
        return self.edge_counts.get(type)

    def add_node(
        self, label: str, key: str, properties: Dict[str, object] = {}
    ) -> str:
        """Adds a new node to the graph with a given label and key type.

        Args:
            label (str): The label to associate with this node.
            key (str): The key to associate with this node.

        Returns:
            str: The new node's ID.
        """
        if key in self._node_keys:
            return -1
        else:
            properties["~label"] = label
            properties["~key"] = key

            if not self._deleted_nodes:
                node_id = uuid4()
                properties["~id"] = node_id
                self._nodes[node_id] = properties
                self._node_keys[key] = node_id
            else:
                # Recycle used nodes before we get fresh ones.
                node_id = self._deleted_nodes.pop()
                properties["~id"] = node_id
                self._nodes.append(properties)
                self._node_keys[key] = node_id

            return node_id

    def remove_node(self, label: str, key: str) -> bool:
        """Removes a node from the graph.

        Args:
            label (string): The label of the node to be removed.
            key (string): The key of the node to be removed.

        Returns:
            bool: [description]
        """

    def get_node_by_id(self, id: str) -> Dict[str, object]:
        """Gets a node's underlying representation by the node-id.

        Args:
            id (str): The node id.

        Returns:
            Dict[str, object]: The node value.
        """
        self._nodes.get(id)

    def get_node_by_label_and_key(
        self, label: str, key: str
    ) -> Union[Dict[str, object], None]:
        """Returns a node's underlying representation by label and key.

        Args:
            label (str): The node label.
            key (str): The node key.

        Returns:
            Union[Dict[str, object], None]: The node value, or None if no
            value present.
        """
        node_id = self._get_node_key_id(label, key)
        if node_id == -1:
            return None

        return self._nodes.get(node_id)

    def get_node_id_by_label_and_key(self, label: str, key: str) -> str:
        """Returns a node's underlying id value by label and key.

        Args:
            label (str): The node label.
            key (str): The node key.

        Returns:
            str: The node id value, or None if no id present.
        """
        return self._get_node_key_id(label, key)

    def get_node_property(
        self, label: str, key: str, property: str
    ) -> Union[Dict[str, object], None]:
        """Get the property for a node by label and key.

        Args:
            label (str): The label of the node.
            key (str): The key of the node.
            property (str): The property to access.

        Returns:
            Union[Dict[str, object], None]: [description]
        """
        node_id = self._get_node_key_id(label, key)
        if node_id == -1:
            return None
        return self._nodes.get(node_id).get(property)

    def update_node_properties(
        self, label: str, key: str, properties: Dict[str, object]
    ) -> bool:
        """Updates node properties with label and key and a list of changes.

        Args:
            label (str): The label of the node whose properties
            will be updated.
            key (str): The key of the node whose properties will be updated.
            properties (Dict[str, object]): The properties to update with.

        Returns:
            bool: True if the properties could be updated, False otherwise.
        """
        node_id = self._get_node_key_id(label, key)
        return self.update_node_properties_by_id(node_id)

    def _get_node_by_key(self, key: str) -> Dict[str, str]:
        """Gets a node by a given key.

        Args:
            key (str): The key to look up.

        Returns:
            Dict[str, str]: The dict associated with the key.
        """
        return self._node_keys.get(key)

    def _get_node_key_id(self, label: str, id: str) -> str:
        """Gets a node by label and id string.

        Args:
            label (str): The node label.
            id (str): The node id.

        Returns:
            str: The node key ID.
        """
        return self._node_keys.get(label).get(id)

    def _remove_node_key_id(self, label: str, id: str):
        """Removes a node from the node keys index by label and id string.

        Args:
            label (str): The node label.
            id (str): The node id.
        """
        if label in self._node_keys:
            del self._node_keys[label]

    def _add_edge_key_id(
        self,
        edge_type: str,
        count: str,
        left_node: str,
        right_node: str,
        id: str,
    ):
        """Adds a edge between a left and right-hand node.
        The edge is an already-known type. Relation represents an edge
        in this case,

        Args:
            edge_type (str): The type of edge being created.
            count (str): The number of edges that exist.
            left_node (str): The left-hand node of the pair.
            right_node (str): The right-hand node of the pair.
            id (str): The ID associating this edge value in the global map.
        """
        edge_key = self._derive_edge_key(edge_type, count)
        self._edge_keys[edge_key] = {
            self._derive_edge_subkey(left_node, right_node): id
        }

    def _get_edge_key_id(
        self, edge_type: str, count: str, left_node: str, right_node: str
    ) -> str:
        """Retrieve a edge by key id.

        Args:
            edge_type (str): The type of edge being looked for.
            count (str): The count of the edge type.
            left_node (str): The left node of the pair.
            right_node (str): The right node of the pair.

        Returns:
            str: The edge key id.
        """
        edge_key = self._derive_edge_key(edge_type, count)
        return self._edge_keys[edge_key].get(
            self._derive_edge_subkey(left_node, right_node)
        )

    def _derive_edge_key(self, edge_type: str, count: int) -> str:
        """Creates the edge key from the type and count.

        Args:
            edge_type (str): The type of edge.
            count (int): The count of the edge.

        Returns:
            str: The edge key
        """
        return f"{edge_type}:{count}"

    def _derive_edge_subkey(self, left_node: str, right_node: str) -> str:
        """Derives an edge subkey.

        Args:
            left_node (str): The left node key.
            right_node (str): The right node key.

        Returns:
            str: The subkey value.
        """
        return f"{left_node}:{right_node}"
