cmake_minimum_required(VERSION 3.13) 
project(AdderClient)

# Find gRPC and Protobuf (the most robust approach)
find_package(gRPC CONFIG REQUIRED)
find_package(Protobuf CONFIG REQUIRED)

# Add generated code directories to your include search path
include_directories(${CMAKE_CURRENT_BINARY_DIR}) 

# Specify your Protocol Buffer definition 
set(PROTO_SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(PROTO_FILE ${PROTO_SRC_DIR}/adder.proto)

# Generate the necessary source and header files from your .proto file
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILE})
grpc_generate_cpp(GRPC_SRCS GRPC_HDRS ${PROTO_FILE})

# Build your client executable 
add_executable(client client.cpp ${PROTO_SRCS} ${PROTO_HDRS} ${GRPC_SRCS} ${GRPC_HDRS})

# Automatically link against required gRPC and Protobuf libraries 
target_link_libraries(client gRPC::grpc++ protobuf::libprotobuf protobuf::libprotoc)
