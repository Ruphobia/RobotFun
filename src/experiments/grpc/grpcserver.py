#!/usr/bin/python3.8
from concurrent import futures
import grpc
import adder_pb2
import adder_pb2_grpc
import time

class AdderServicer(adder_pb2_grpc.AdderServicer):
    def AddNumbers(self, request, context):
        return adder_pb2.AddReply(sum=request.number1 + request.number2)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    adder_pb2_grpc.add_AdderServicer_to_server(AdderServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
