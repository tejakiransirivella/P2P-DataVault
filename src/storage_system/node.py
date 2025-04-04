import json
from datetime import datetime


class Node:
    __slots__ = "ip_address", "udp_port", "node_id", "timestamp", "level"

    def __init__(self, ip_address, udp_port, node_id):
        self.ip_address = ip_address
        self.udp_port = udp_port
        self.node_id = node_id
        self.timestamp = datetime.utcnow()
        self.level = None

    def __str__(self):
        # return self.ip_address + " " + str(self.udp_port) + " " + str(self.node_id) + " " + str(self.timestamp)
        return json.dumps({
            'ip_address': self.ip_address,
            'udp_port': self.udp_port,
            'node_id' : self.node_id,
            'level' : self.level,
            'timestamp' : str(self.timestamp)
        }, indent=4)
