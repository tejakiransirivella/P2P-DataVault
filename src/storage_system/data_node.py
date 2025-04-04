class data_node:
    __slots__ = "k_buckets", "length"

    def __init__(self, length):
        self.k_buckets = []
        self.length = length

    def append(self, node, k):
        if len(self.k_buckets) > k:
            return
        self.k_buckets.append(node)
        self.k_buckets = sorted(self.k_buckets, key=lambda x: x.timestamp, reverse=True)

    def __str__(self):
        nodes = ""
        for node in self.k_buckets:
            nodes = nodes + str(node) + "\n"
        return nodes
