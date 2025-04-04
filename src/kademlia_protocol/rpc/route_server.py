import grpc
import route_pb2
import route_pb2_grpc
from concurrent import futures
from Distributed_Storage_System.protocol import Protocol
from Distributed_Storage_System.kademlia_protocol import initiate_startup


class RouterService(route_pb2_grpc.RouterServicer):
    protocol_obj: Protocol

    def __init__(self):
        self.protocol_obj = Protocol()
        initiate_startup()

    def Lookup(self, request, context):
        final_k_closest = self.protocol_obj.lookup(request.id, context.peer())

        for k in final_k_closest:
            yield route_pb2.LookupResponse(k.ip_address, k.udp_port, k.node_id)

    def FindNode(self, request, context):
        final_k_closest = self.protocol_obj.find_node(request.id)

        for k in final_k_closest:
            yield route_pb2.FindNodeResponse(k.ip_address, k.udp_port, k.node_id)

    def FindValue(self, request, context):
        return route_pb2.FindValueResponse(value=self.protocol_obj.find_value(request.id))

    def Ping(self, request, context):
        pass

    def Store(self, request, context):
        return route_pb2.StoreResponse(self.protocol_obj.store(request.key, request.value))

    def TestRouter(self, request, context):
        message = f"Hello {request.name}"
        return route_pb2.TestResponse(message=message)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    route_pb2_grpc.add_RouterServicer_to_server(RouterService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server Started!")
    server.wait_for_termination()


if __name__ == '__main__':
    main()
