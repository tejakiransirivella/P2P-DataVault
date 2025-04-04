import json
import os.path
import socket

import grpc

import util
from Distributed_Storage_System.test import node
from kademlia.rpc import route_pb2_grpc, route_pb2
from node import Node
from protocol import Protocol
from routing_table import routing_table


def initiate_startup():
    current_node_id = util.generate_random_node_id()
    current_node = Node(socket.gethostbyname(socket.gethostname()), util.PORT, current_node_id)

    table = routing_table()
    table.owner_node = current_node

    # k_protocol = Protocol()
    # k_protocol.table = table

    if os.path.exists('/bootstrap.json'):
        # RPC on bootstrap node on owner node id
        bootstrap_node = load_bootstrap_info()
        generate_routing_table(table, bootstrap_node)
        channel = grpc.insecure_channel(f'{bootstrap_node.ip_address}:{bootstrap_node.udp_port}')
        stub = route_pb2_grpc.RouterStub(channel)
        final_k_closest = stub.Lookup(route_pb2.LookupRequest(id=bootstrap_node.node_id))  # result from RPC call

        for node_tuple in final_k_closest:
            closest_node = Node(node_tuple[0], node_tuple[1], node_tuple[2])
            Protocol.table.insert_node(closest_node)
    else:
        generate_routing_table(table, None)

    print(table)

def load_bootstrap_info():
    with open('bootstrap.json', 'r') as json_file:
        bootstrap_node_info = json.load(json_file)
        bootstrap_node = Node(bootstrap_node_info['ip_address'],
                              bootstrap_node_info['port'], bootstrap_node_info['node_id'])
        return bootstrap_node


def generate_routing_table(table, bootstrap_node):
    table.generate_prefix_tree(util.BIT_LENGTH)

    # fill bootstrap node in the routing table

    if bootstrap_node is not None:
        table.insert_node(bootstrap_node)


initiate_startup()
