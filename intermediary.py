#!/bin/python3

from socket import socket, AF_INET, SOCK_STREAM
import random
import sys
import select

if (len(sys.argv) != 2):
    print("Usage: python3 intermediary.py <port>")
    sys.exit(1)

PUBLIC_PORT =   int(sys.argv[1])
HOST        =   'localhost'
MAX_CLIENTS =   1024

class Server:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.inputs = [self.socket]
        self.outputs = []
        self.msg_queues = {}
        self._all_clients = {}

    def run(self):
        self.bind()
        self.listen()
        while (self.inputs):
            print("Waiting for a client to connect on the port {}...".format(PUBLIC_PORT))
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            self.read(readable)
            self.write(writeable)

    def generate_ports(self):
        ports = []
        for i in range(0, 10):
            ports.append(random.randint(1024, 65535))
        return ports

    def write(self, writeable):
        for s in writeable:
            try:
                next_msg = self.msg_queues[s].get_nowait()
            except Queue.Empty:
                self.outputs.remove(s)
            else:
                s.send(next_msg)

    def read(self, readable):
        for s in readable:
            if s is self.socket:
                connection, client_address = s.accept()
                connection.setblocking(0)
                self.inputs.append(connection)
                self._all_clients[connection] = self.generate_ports()
                print("All ports available for the client {}: {}".format(client_address, self._all_clients[connection]))

            else:
                data = s.recv(1024)
                if data:
                    print("Received data from the client {}: {}".format(s.getpeername(), data.decode()))
                    if (data.decode() == "exit"):
                        self.inputs.remove(s)
                        s.close()
                else:
                    self.inputs.remove(s)
                    s.close()
    def bind(self):
        self.socket.bind((HOST, PUBLIC_PORT))

    def listen(self):
        self.socket.listen(MAX_CLIENTS)


if __name__ == "__main__":
    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        print("Closing the server...")
        sys.exit(0)
