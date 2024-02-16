#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>
#include "adder.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using adder::AddRequest;
using adder::AddReply;
using adder::Adder;

class AdderClient {
public:
    AdderClient(std::shared_ptr<Channel> channel) : stub_(Adder::NewStub(channel)) {}

    // Assembles the client's payload, sends it and presents the response back from the server.
    int AddNumbers(int number1, int number2) {
        // Data we are sending to the server.
        AddRequest request;
        request.set_number1(number1);
        request.set_number2(number2);

        // Container for the data we expect from the server.
        AddReply reply;

        // Context for the client.
        ClientContext context;

        // The actual RPC.
        Status status = stub_->AddNumbers(&context, request, &reply);

        // Act upon its status.
        if (status.ok()) {
            return reply.sum();
        } else {
            std::cout << status.error_code() << ": " << status.error_message()
                      << std::endl;
            return 0;
        }
    }

private:
    std::unique_ptr<Adder::Stub> stub_;
};

int main(int argc, char** argv) {
    // Instantiate the client. It requires a channel, out of which the actual RPCs
    // are created. This channel models a connection to an endpoint specified by
    // the argument "--target=" which is the server address and port.
    AdderClient adder(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
    int number1 = 10;  // Example number1
    int number2 = 20;  // Example number2

    std::cout << "Attempting to add " << number1 << " and " << number2 << std::endl;
    int sum = adder.AddNumbers(number1, number2);
    std::cout << "Sum: " << sum << std::endl;

    return 0;
}
