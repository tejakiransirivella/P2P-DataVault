import grpc

import util
from Distributed_Storage_System.node import Node
from kademlia.rpc import route_pb2_grpc, route_pb2
from routing_table import routing_table



class Protocol:
    __slots__ = "table", "files"

    table: routing_table

    def __init__(self):
        self.table = None
        self.files = dict()

    def lookup(self, node_id, peer_id):

        # insert the node_id in the tree
        peer = peer_id.split(":")
        cl_node = Node(peer[1], int(peer[2]), node_id)
        self.table.insert_node(cl_node)

        k_closest_nodes = self.table.find_k_closest_nodes(node_id)
        final_k_closest = [k_closest_nodes]
        for node in k_closest_nodes:
            # RPC call here
            channel = grpc.insecure_channel(f'{node[0]}:{node[1]}')
            stub = route_pb2_grpc.RouterStub(channel)
            k_nodes = stub.Lookup(route_pb2.FindRequest(id=node[2]))  # result from RPC call
            final_k_closest.extend(k_nodes)
            final_k_closest = sorted(final_k_closest, key=lambda x: util.xor_distance(x[2], node_id))
            final_k_closest = final_k_closest[0:self.table.k]
        return final_k_closest

    def find_node(self, node_id):
        k_closest_nodes = self.table.find_k_closest_nodes(node_id)
        final_k_closest = [k_closest_nodes]
        for node in k_closest_nodes:
            # RPC call here
            channel = grpc.insecure_channel(f'{node[0]}:{node[1]}')
            stub = route_pb2_grpc.RouterStub(channel)
            k_nodes = stub.FindNode(route_pb2.FindRequest(id=node[2]))  # result from RPC call
            final_k_closest.extend(k_nodes)
            final_k_closest = sorted(final_k_closest, key=lambda x: util.xor_distance(x[2], node_id))
            final_k_closest = final_k_closest[0:self.table.k]
        return final_k_closest

    def find_value(self, file_id):
        value = self.files.get(file_id)
        if value is None:
            # handle error
            pass
        else:
            return value

    def store(self, file_id, data):

        # RPC on store
        self.files[file_id] = data

    # def test(self):
    #     k_closest = self.find_node(file_id)
    #     closest_node = k_closest[0]
