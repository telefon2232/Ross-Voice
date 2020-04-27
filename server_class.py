import threading
import socket
main_port = 4999


class Server:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dict_room = {}
        self.port_room = main_port + 1
        self.sock = sock
        self.sock.bind(('0.0.0.0', main_port)) #port 4999 listen main channel

    def get_link(self):
        import random
        password = ''
        for i in range(50):
            password += chr(random.randint(65, 123))
        # 65-122
        return password

    def main_room(self):
        while True:
            data, address = self.sock.recvfrom(100)
            if data == b'create_room':
                name_room = self.get_link()
                self.sock.sendto(bytes(name_room.encode('utf-8')), address)
                threading.Thread(target=self.create_room, args=(name_room,)).start()
            if len(data.decode('utf-8')) == 50:

                if self.dict_room.get(data.decode('utf-8')) is not None:
                    aa = self.dict_room.get(data.decode('utf-8'))
                    aa=(bytes( str(aa).encode('utf-8')))
                    self.sock.sendto(aa, address)
                    print('connected')

    def create_room(self,name_room):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.bind(('0.0.0.0', self.port_room))
        clients = []
        self.dict_room[name_room] = self.port_room

        self.port_room += 1
        while True:
            data, address = s.recvfrom(4096)

            if address not in clients:
                clients.append(address)
                print(str(address) + ' connected!')
            for user in clients:
                if user == address:  #
                    continue
                s.sendto(data, user)
                print(data,user)

a = Server()
a.main_room()
