from dsu import DSU
from segment_tree import SegmentTree


class Network:
    """
    Small DSA model for a monitored connection:
    node 0 = monitoring laptop, node 1 = monitored laptop.
    The link is active only when the monitored endpoint is reachable.
    """
    def __init__(self):
        self.names = ["Monitor Laptop", "Remote Laptop"]
        self.up = [True, False]
        self.latency = [0.0, 0.0]
        self.edges = [(0, 1, False)]  # (node A, node B, active)
        self.dsu = DSU(2)
        self.dsu_dirty = True
        self.segment_tree = SegmentTree([not x for x in self.up], self.latency)

    def set_remote_status(self, is_up, latency_ms=0.0):
        changed = self.up[1] != is_up
        self.up[1] = is_up
        self.latency[1] = latency_ms if is_up else 0.0
        self.edges[0] = (0, 1, is_up and self.up[0])
        if changed:
            self.dsu_dirty = True
        self.segment_tree.update(1, failed=not is_up, latency=self.latency[1])

    def _rebuild_dsu(self):
        self.dsu = DSU(len(self.names))
        for a, b, active in self.edges:
            if active and self.up[a] and self.up[b]:
                self.dsu.union(a, b)
        self.dsu_dirty = False

    def are_connected(self, a, b):
        if self.dsu_dirty:
            self._rebuild_dsu()
        if not self.up[a] or not self.up[b]:
            return False
        return self.dsu.find(a) == self.dsu.find(b)

    def component_count(self):
        if self.dsu_dirty:
            self._rebuild_dsu()
        # Count only online nodes as components; offline nodes are reported separately.
        roots = set()
        for i, is_up in enumerate(self.up):
            if is_up:
                roots.add(self.dsu.find(i))
        return len(roots)

    def failed_count(self):
        return self.segment_tree.count_failed(0, len(self.names) - 1)

    def max_latency(self):
        return self.segment_tree.max_latency(0, len(self.names) - 1)
