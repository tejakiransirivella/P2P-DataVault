import util
from bit_node import bit_node
from data_node import data_node


class routing_table:
    __slots__ = "root", "owner_node", "k"

    def __init__(self):
        self.root = None
        self.owner_node = None
        self.k = 5

    def parse(self, root, output_nodes):
        if isinstance(root, data_node):
            output_nodes.extend(root.k_buckets)
            return
        self.parse(root.left, output_nodes)
        self.parse(root.right, output_nodes)

    def prefix_tree_helper(self, root, current_level):
        if current_level == 1:
            root.left = data_node(0)
        else:
            root.left = bit_node()

        if isinstance(root.left, bit_node):
            self.prefix_tree_helper(root.left, current_level - 1)
        root.right = data_node(2 ** (current_level - 1))

    def generate_prefix_tree(self, level):
        self.root = bit_node()
        self.prefix_tree_helper(self.root, level)

    def insert_node(self, node):
        distance = util.xor_distance(self.owner_node, node)
        self.insert_node_helper(self.root, node, distance, 0)

    def insert_node_helper(self, root, node, distance, level):
        if isinstance(root, data_node):
            node.level = level
            root.append(node, self.k)
        elif distance[level] == '0':
            self.insert_node_helper(root.left, node, distance, level + 1)
        else:
            self.insert_node_helper(root.right, node, distance, level + 1)

    def find_k_closest_nodes(self, node_id):
        distance = util.xor_distance(self.owner_node, node_id)
        k_buckets = self.traverse_table(self.root, distance, 0)
        k_closest_nodes = []
        for k_bucket in k_buckets:
            k_closest_nodes.append((k_bucket.ip_address, k_bucket.udp_port, k_bucket.node_id))
        return k_closest_nodes

    def traverse_table(self, root, distance, level):
        if isinstance(root, data_node):
            return root.k_buckets
        elif distance[level] == '0':
            return self.traverse_table(root.left, distance, level + 1)
        else:
            return self.traverse_table(root.right, distance, level + 1)

    def __str__(self):
        output_nodes = []
        self.parse(self.root, output_nodes)
        output = ""
        for output_node in output_nodes:
            output = output + str(output_node) + "\n"
        return output
