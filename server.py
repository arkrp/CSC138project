#Nicolas Gugliemo
#Garret Learned
#Hannah Nelson
#Fabrice Auriole Yonkeu Ebenye
#Estefany Aguilar Luna
#CSC/CPE 138 Section 01
#11/26/2023
#server program for the TCP chatroom

import socket
import sys
import threading

users = {}
svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def create_server(port):  # Create server and bind port to IP; start listening
    svr_socket.bind(("0.0.0.0", port))
    svr_socket.listen(1)
    print('The Chat Server Started')

    while True:
        user_socket, user_address = svr_socket.accept()
        print(f"Connected with {user_socket}, {user_address}")

        user_thread = threading.Thread(target=handle_user, args=(user_socket, user_address))
        user_thread.start()


def handle_user(user_socket, address):
    sender = None

    while True:
        incoming = user_socket.recv(1024).decode('utf-8').strip()
        command, *args = incoming.split()

        if command == "JOIN":
            JOIN(name=args[0], user_socket=user_socket, address=address)
            sender = args[0]  # Update sender when JOIN command is processed
        elif command == "LIST":
            LIST(user_socket)
        elif command == "MESG":
            MESG(sender, *args)
        elif command == "BCST":
            BCST(sender=args[0], message=args[1])
        elif command == "QUIT":
            QUIT(user_socket=user_socket)
        else:
            user_socket.send("Unknown Message".encode("utf-8"))


def JOIN(name, user_socket, address):
    print('Attempting to have user join')
    print(f'Connected with {str(address)}')
    if len(users) >= 10:
        user_socket.send('Too Many Users'.encode('utf-8'))
    else:
        if name in users:
            user_socket.send("Name already taken, or already joined".encode("utf-8"))
        else:
            users[str(name)] = user_socket
            print(f'The name of this client is {name}'.encode('utf-8'))
            BCST(user_socket, f'{str(name)} has Joined the Chatroom'.encode('utf-8'))
            user_socket.send('You are connected'.encode('utf-8'))


def BCST(sender, message):
    for name, user_socket in users.items():
        if name != sender:
            user_socket.send(f'{str(name)} is sending a broadcast\n {message}'.encode('utf-8'))


def QUIT(user_socket):
    # Find the name associated with the given user_socket
    name = find_name_by_socket(users, user_socket)

    if name is not None:
        print(f"{name} has left the chat.")
        BCST(user_socket, f'{name} is quitting the chat server'.encode('utf-8'))
        del users[name]
        user_socket.close()
        sys.exit(0)
    else:
        print("User not found for QUIT command.")

    try:
        # Check if the socket is still valid before sending a message
        if user_socket.fileno() != -1:
            user_socket.send("You are not registered or already left.".encode('utf-8'))
    except OSError as e:
        print(f"Error: {e}")

def LIST(user_socket):
    user_list = "\n".join(str(name) for name in users.keys())
    user_socket.send(user_list.encode('utf-8'))
    print("List has been sent")
    print(user_list)


def MESG(sender, *args):
    try:
        if len(args) < 2:
            raise ValueError("MESG command requires at least two arguments: recipientName and message")

        recipientName, message = args

        if recipientName in users:
            rec_socket = users[recipientName]
            rec_socket.send(f'Message from {sender}: {message}'.encode('utf-8'))
        else:
            users[sender].send(f'This recipient name is not in the chat room'.encode('utf-8'))

    except ValueError as ve:
        users[sender].send(f'Error: {ve}'.encode('utf-8'))

    except Exception as e:
        print(f"Error processing MESG command: {e}")
        users[sender].send(f"An error occurred while processing MESG command".encode('utf-8'))

def find_name_by_socket(users, target_socket):
    for name, socket_obj in users.items():
        if socket_obj == target_socket:
            return name
    return None  # Return None if the socket object is not found

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <svr_port>")
        sys.exit(1)

    port = int(sys.argv[1])
    create_server(port)


if __name__ == "__main__":
    main()
