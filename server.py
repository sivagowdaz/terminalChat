import socket
import threading
from utilityClasses import User, Room
import time


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = 'Disconnect'
HEADER = 64
FORMATE = 'utf-8'

thread = None

rooms = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def recieveMessage(user):
    msg = user.conn.recv(int(1024)).decode(FORMATE)
    return msg


def boradCastMessage(room, message):
    for user in room.connections:
        user.conn.send(message.encode(FORMATE))


def createRoom(user):
    msg = recieveMessage(user)
    roomId, roomName = msg.split(",")
    if not roomId in rooms.keys():
        room = Room(roomName, roomId, user)
        user.conn.send(
            f"[NOTIFICATION] Room is created with id{room.roomId}".encode(FORMATE))
        rooms[roomId] = room
        print(f"Room is created with id {room.roomId}")
        user.conn.send("SUCCESS".encode(FORMATE))
        return room
    else:
        user.conn.send(
            f"[NOTIFICATION] This room id {roomId} is already taken".encode(FORMATE))
        time.sleep(0.1)
        user.conn.send("FAILURE".encode(FORMATE))


def joinRoom(user):
    roomId = recieveMessage(user)
    room = rooms.get(roomId, False)
    if room:
        room.connections.append(user)
        message = f"[NOTIFICATION] {user.userName} joined"
        boradCastMessage(room, message)
        user.conn.send("SUCCESS".encode(FORMATE))
        return room
    else:
        user.conn.send(
            f"Room with roomId {roomId} does not exists".encode(FORMATE))
        time.sleep(0.1)
        user.conn.send("FAILURE".encode(FORMATE))


def conductChat(user, room):
    while room:
        message = recieveMessage(user)
        if message == DISCONNECT_MESSAGE or message == 'quit':
            message = f"{user.userName} disconnected"
            boradCastMessage(room, message)
            room.connections.remove(user)
            room = None
        else:
            message = f"[{user.userName}] {message}"
            boradCastMessage(room, message)


def handleClient(conn, addr):
    print("New Connection ", addr)
    conn.send('Connection Successful'.encode(FORMATE))
    username = conn.recv(1024).decode(FORMATE)
    user = User(username, conn)
    while True:
        msg = recieveMessage(user)
        room = None

        if msg == 'CREATE ROOM':
            room = createRoom(user)
        elif msg == 'JOIN ROOM':
            room = joinRoom(user)

        conductChat(user, room)


def connectToClient():
    server.listen()
    print(f"{SERVER} is listening on port {PORT}")
    global thread
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print("NUMBR OF THREADS", threading.active_count())


connectToClient()
