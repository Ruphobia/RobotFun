#!/usr/bin/python3.8
import grpc
import adder_pb2
import adder_pb2_grpc
import random
import time

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = adder_pb2_grpc.AdderStub(channel)
        while True:
            number1 = random.randint(1, 100)
            number2 = random.randint(1, 100)
            response = stub.AddNumbers(adder_pb2.AddRequest(number1=number1, number2=number2))
            print(f"Sum of {number1} and {number2} is {response.sum}")
          
if __name__ == '__main__':
    run()
