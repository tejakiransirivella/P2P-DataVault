import hashlib
import json
import random
import secrets
import socket

import util
from node import node

PORT = 8080
BIT_LENGTH = 4


def generate_random_node_id():
    no_of_bytes = random.randint(1, 20)
    node_id = secrets.token_hex(no_of_bytes)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(bytes.fromhex(node_id))
    node_id = int(sha256_hash.hexdigest(), 16)
    node_id = node_id & (2 ** BIT_LENGTH - 1)
    return node_id


def generate_bootstrap_node_info():
    bootstrap_data = {"ip_address": socket.gethostbyname(socket.gethostname()),
                      "port": PORT,
                      "node_id": generate_random_node_id(4)}

    with open('bootstrap.json', 'w') as json_file:
        json.dump(bootstrap_data, json_file, indent=4)


def xor_distance(node1: node, node2: node):
    distance = bin(node1.node_id ^ node2.node_id)[2:]
    distance = distance.zfill(util.BIT_LENGTH)
    # print(distance)
    return distance


def main():
    generate_bootstrap_node_info()


if __name__ == "__main__":
    main()
