import grpc
import route_pb2
import route_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = route_pb2_grpc.RouterStub(channel)
        response = stub.TestRouter.future(route_pb2.TestRequest(name="Ashwin Kherde"))
        print(response.result())


if __name__ == '__main__':
    run()
