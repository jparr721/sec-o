from collections import defaultdict
from typing import Dict, List

from pyroaring import BitMap

from .reversible_multi_map import ReversibleMultiMap


class Graph:
    """The graph structure repsents a traversable, in-memory graph for
    arranging related data by left->edge->[right] connections. It
    features a bi-directional multimap under the hood to make left-hand
    lookups and right-hand lookups very efficient.

    It maintains reference structures to underlying node data to allow for
    the bi-directional multimap to focus on relationships, fetching underlying
    data only when absolutely necessary.
    """

    def __init__(self):
        self._node_keys: Dict[str, Dict[str, int]] = defaultdict(
            defaultdict(int)
        )
        self._nodes: List[Dict[str, object]] = []
        self._relationship_keys: Dict[int, int] = defaultdict(int)
        self._relationships: List[Dict[str, object]] = []
        self._related: Dict[str, ReversibleMultiMap] = defaultdict(
            ReversibleMultiMap
        )
