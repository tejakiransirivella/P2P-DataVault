# **📌P2P-DataVault**

A decentralized, peer-to-peer storage system that prioritizes scalability, availability, and security. This platform breaks large files into encrypted blocks, distributes them across peer nodes, and ensures fault-tolerance through replication—all powered by **Kademlia DHT and gRPC**.

## **✨Key Features**
- Leveraging peer-to-peer architecture to avoid central points of failure.
- Using Kademlia for efficient object lookup and node discovery.
- Encrypting data with AES-256 + HMAC for confidentiality and integrity.
- Efficient peer-to-peer synchronization

## **🚧Current Work (In Progress)**
- Working on developing a Python-based decentralized storage application, leveraging Kademlia Distributed Hash table (DHT) for efficient,fault-tolerant decentralized lookup of data files, ensuring high scalability and availability.
- Implementing high-performance gRPC communication protocols to facilitate reliable, low-latency data transfer and synchronization between distributed peers in the network.

## **🌍User Impact (Projected)**
- Improved data accessibility by 40%
- Reduced storage infrastructure costs
- Enhanced fault tolerance
- Enables seamless distributed file management

## **⚡Quick Start**
```bash
# Clone the repository
git clone https://github.com/yourusername/p2p-storage.git
cd p2p-storage

# Setup environment
pip install -r requirements.txt

```

Configure bootstrap.json with initial network nodes

```bash
# Initialise peer network
python src/distributed_client.py
```

Manage file storage via GUI or CLI

## **🗂️Project Structure**
```
P2P-DATAVAULT/
│
├── src/
│   ├── datastore/
│   ├── distributed_client.py
│   ├── file_operations.py
│   ├── gui.py
│   │
│   ├── kademlia_protocol/
│   │   └── rpc/
│   │       ├── route_client.py
│   │       ├── route_pb2.py
│   │       └── route_server.py
│   │
│   └── storage_system/
│       ├── bit_node.py
│       ├── data_node.py
│       └── kademlia_protocol.py
│
└── README.md
```

---
