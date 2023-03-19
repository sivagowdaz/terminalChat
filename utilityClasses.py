class User:
    def __init__(self, userName=None, conn=None):
        self.userName = userName
        self.conn = conn


class Room:
    def __init__(self, roomName=None, roomId=None, conn=None):
        self.roomName = roomName
        self.roomId = roomId
        self.connections = [conn]
