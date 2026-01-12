import grpc

gRPC_server = "localhost"
gRPC_server_port = 50051

channel = grpc.insecure_channel(f"{gRPC_server}:{gRPC_server_port}")
