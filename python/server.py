import grpc
import example_pb2
import example_pb2_grpc
from concurrent import futures
from statistics import mean, median, mode
import time


class ExampleServicer(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        response = example_pb2.HelloResponse()
        response.reply = "Hello " + request.greeting + "!"
        return response

    def DoAddition(self, request, context):
        response = example_pb2.NumberResponse()
        response.result = request.first_number + request.second_number
        return response

    def DoSubtraction(self, request, context):
        response = example_pb2.NumberResponse()
        response.result = request.first_number - request.second_number
        return response

    def ComputeCentralOfFive(self, data, context):
        print('a:', data.a)
        print('b:', data.b)
        print('c:', data.c)
        print('d:', data.d)
        print('e:', data.e)

        data = [data.a, data.b, data.c, data.d, data.e]

        centrals = example_pb2.CentralTendency()
        centrals.mean = mean(data)
        centrals.median = median(data)
        centrals.mode = mode(data)

        return centrals
        


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    example_pb2_grpc.add_ExampleServiceServicer_to_server(
        ExampleServicer(), server)

    print('Starting server. Listening on port 50050.')
    server.add_insecure_port('[::]:50050')
    server.start()

    try:
        while True:
            time.sleep(86400)

    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()
