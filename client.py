import socket
import threading

PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOST, PORT)
FORMATE = 'utf-8'
HEADER = 64

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendMessage(msg):
    message = msg.encode(FORMATE)
    client.send(message)


def EnterRoom():
    connected = True
    print("1. CREATE ROOM\n2. JOIN ROOM\n")
    option = int(input())
    if option == 1:
        roomId = int(input("Enter the room Id you want to create"))
        roomName = input("Name of the room")
        sendMessage('CREATE ROOM')
        sendMessage(f"{roomId},{roomName}")
        print(client.recv(1024).decode(FORMATE))
        msg = client.recv(1024).decode(FORMATE)
        print("message is", msg)
        if msg != 'SUCCESS':
            connected = False
    elif option == 2:
        roomId = int(input("Enter the room Id you want to join"))
        sendMessage('JOIN ROOM')
        sendMessage(f"{roomId}")
        print(client.recv(1024).decode(FORMATE))
        msg = client.recv(1024).decode(FORMATE)
        if msg != 'SUCCESS':
            connected = False
    else:
        print("Invalid input")
        connected = False

    while connected:
        thread = threading.Thread(target=getMessage)
        thread.daemon = True
        thread.start()
        msg = input("Eter the text\n")
        sendMessage(msg)
        if msg == "Disconnect":
            break
        if msg == 'quit':
            quit()


def getMessage():
    while True:
        message = client.recv(1024).decode(FORMATE)
        print(f"{message}\n")


def interactServer():
    client.connect(ADDRESS)
    print(client.recv(1000).decode(FORMATE))
    userName = input("Provide the username")
    client.send(userName.encode(FORMATE))
    while True:
        EnterRoom()


interactServer()
