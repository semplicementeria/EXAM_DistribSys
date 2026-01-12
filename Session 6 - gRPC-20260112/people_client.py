import people_pb2
import people_pb2_grpc
import argparse

# This is where we can configure which gRPC server we want to connect to
from people_conf import channel

def run_client(action, user_name, user_email, user_id):
    
    stub = people_pb2_grpc.UserServiceStub(channel)

    if action == "add":
        # Create a user
        response = stub.CreateUser(people_pb2.CreateUserRequest(name=user_name, email=user_email))
        user_id = response.id
        print(f"{response.message} - ID = {user_id}")

    elif action == "get":
        if user_id:
            # Retrieve specified User
            user = stub.GetUserById(people_pb2.UserIdRequest(id=user_id))
            if user.id:
                print(f"User: ID={user.id}, Name={user.name}, Email={user.email}")
        else:
            # Retrieve all users
            user_list = stub.GetAllUsers(people_pb2.Empty())
            print(f"List of retrieved users:\n")
            for user in user_list.user:
                print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
            print(f"\n{len(user_list.user)} users retrieved")

    elif action == "mod":
        # Update user details
        update_response = stub.UpdateUser(people_pb2.User(id=user_id, name=user_name, email=user_email))
        print(update_response.message)

    elif action == "del":
        # Delete user
        delete_response = stub.DeleteUserById(people_pb2.UserIdRequest(id=user_id))
        print(delete_response.message)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simple gRPC-based user management interactive script.")
    parser.add_argument('action', metavar='ACTION', type=str, choices=['add', 'del', 'mod', 'get'], help='Action to be executed on the specified user')
    parser.add_argument('-n', '--name', metavar='NAME', type=str, help='User name')
    parser.add_argument('-e', '--email', metavar='EMAIL', type=str, help='User email')
    parser.add_argument('-i', '--id', metavar='ID', type=str, help='User ID')
    args = parser.parse_args()
    if args.action == "add" and (args.name is None or args.email is None):
        parser.error("Both name and email are required when adding a new user.")
    elif args.action == "del" and args.id is None:
        parser.error("User ID is required when deleting a user.")
    elif args.action == "mod" and args.id is None:
        parser.error("User ID is required when updating a user.")

    run_client(args.action, args.name, args.email, args.id)
