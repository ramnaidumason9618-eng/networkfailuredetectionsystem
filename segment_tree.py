class SegmentTree:
    # Each position stores: (failed_node_count, maximum_latency_ms)
    def __init__(self, failed, latency):
        self.n = len(failed)
        size = max(1, 4 * self.n)
        self.failed_tree = [0] * size
        self.latency_tree = [0.0] * size

        if self.n > 0:
            self._build(1, 0, self.n - 1, failed, latency)

    def _build(self, node, left, right, failed, latency):
        if left == right:
            self.failed_tree[node] = 1 if failed[left] else 0
            self.latency_tree[node] = latency[left]
            return

        mid = (left + right) // 2
        self._build(node * 2, left, mid, failed, latency)
        self._build(node * 2 + 1, mid + 1, right, failed, latency)
        self._pull(node)

    def _pull(self, node):
        self.failed_tree[node] = (
            self.failed_tree[node * 2] + self.failed_tree[node * 2 + 1]
        )
        self.latency_tree[node] = max(
            self.latency_tree[node * 2],
            self.latency_tree[node * 2 + 1]
        )

    def update(self, index, failed=None, latency=None):
        if self.n == 0 or index < 0 or index >= self.n:
            return
        self._update(1, 0, self.n - 1, index, failed, latency)

    def _update(self, node, left, right, index, failed, latency):
        if left == right:
            if failed is not None:
                self.failed_tree[node] = 1 if failed else 0
            if latency is not None:
                self.latency_tree[node] = latency
            return

        mid = (left + right) // 2
        if index <= mid:
            self._update(node * 2, left, mid, index, failed, latency)
        else:
            self._update(node * 2 + 1, mid + 1, right, index, failed, latency)
        self._pull(node)

    def count_failed(self, query_left, query_right):
        if self.n == 0:
            return 0
        query_left = max(0, query_left)
        query_right = min(self.n - 1, query_right)
        if query_left > query_right:
            return 0
        return self._count(1, 0, self.n - 1, query_left, query_right)

    def _count(self, node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return self.failed_tree[node]
        if right < ql or left > qr:
            return 0
        mid = (left + right) // 2
        return (
            self._count(node * 2, left, mid, ql, qr)
            + self._count(node * 2 + 1, mid + 1, right, ql, qr)
        )

    def max_latency(self, query_left, query_right):
        if self.n == 0:
            return 0.0
        query_left = max(0, query_left)
        query_right = min(self.n - 1, query_right)
        if query_left > query_right:
            return 0.0
        return self._max(1, 0, self.n - 1, query_left, query_right)

    def _max(self, node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return self.latency_tree[node]
        if right < ql or left > qr:
            return 0.0
        mid = (left + right) // 2
        return max(
            self._max(node * 2, left, mid, ql, qr),
            self._max(node * 2 + 1, mid + 1, right, ql, qr)
        )
