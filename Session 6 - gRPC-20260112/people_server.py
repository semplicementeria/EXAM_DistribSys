import grpc
import uuid
import people_pb2
import people_pb2_grpc
from concurrent import futures

class UserService(people_pb2_grpc.UserServiceServicer):
    """
    Implementation of the gRPC UserService.
    This service manages user creation, retrieval, modification, and deletion.
    """
    
    def __init__(self):
        # Dictionary to store user data with unique user_id as key
        self.users = {}  # Example: {"user_id": {"name": "Alice", "email": "alice@example.com"}}

    def GetAllUsers(self, request, context):
        """
        Retrieve all users in the system.
        Returns a UserList message containing all registered users.
        """
        users_list = [
            people_pb2.User(id=user_id, name=user["name"], email=user["email"])
            for user_id, user in self.users.items()
        ]
        return people_pb2.UserList(user=users_list)

    def CreateUser(self, request, context):
        """
        Create a new user with a unique UUID, name, and email.
        Returns a UserResponse containing the new user's ID and a success message.
        """
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        self.users[user_id] = {"name": request.name, "email": request.email}
        
        return people_pb2.CreateUserResponse(
            id=user_id,
            message="User created successfully"
        )

    def GetUserById(self, request, context):
        """
        Retrieve a user's details by their unique ID.
        If the user is found, return their information as a User message.
        If the user is not found, return a NOT_FOUND gRPC status.
        """
        user = self.users.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {request.id} not found")
            return people_pb2.User()  # Return empty user object if not found

        return people_pb2.User(
            id=request.id,
            name=user["name"],
            email=user["email"]
        )
    
    def UpdateUser(self, request, context):
        """
        Update an existing user's details.
        Only updates fields that are provided in the request (name/email).
        If the user does not exist, returns a NOT_FOUND gRPC status.
        """
        user = self.users.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {request.id} not found")
            return people_pb2.UpdateUserResponse(message="User not found")

        # Update user details if provided
        if request.name:
            user["name"] = request.name
        if request.email:
            user["email"] = request.email

        return people_pb2.UpdateUserResponse(
            message=f"User with ID {request.id} updated successfully"
        )

    def DeleteUserById(self, request, context):
        """
        Delete a user by their unique ID.
        If the user exists, they are removed, and a confirmation message is returned.
        If the user does not exist, a NOT_FOUND gRPC status is returned.
        """
        if request.id in self.users:
            del self.users[request.id]
            return people_pb2.UpdateUserResponse(
                message=f"User with ID {request.id} deleted successfully"
            )

        # User not found, return NOT_FOUND status
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f"User with ID {request.id} not found")
        return people_pb2.UpdateUserResponse(message="")


def serve():
    """
    Start the gRPC server and listen for client requests.
    The server runs on port 50051 and handles multiple requests using a thread pool.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Multi-threaded server

    # Add a servicer to the server, with the RPC methods specified in the Protocol Buffer file
    people_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    
    # Start listening on all interfaces on port 50051
    server.add_insecure_port("[::]:50051")
    server.start()
    
    try:
        print("User Management gRPC Server is running on port 50051...")
        server.wait_for_termination()

    except KeyboardInterrupt:
        print("The server is terminating...")


if __name__ == "__main__":
    serve() # Run the server when executed
