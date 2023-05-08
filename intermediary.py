#!/bin/python3

import socket
import select
import threading
import random
import time

LOCALHOST = "localhost"
PORT = 4243

class Server:
    def __init__(self):
        self._client_lists = []
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ports_list = []
        self._port = PORT


    def _run_another_server(self, client_socket, ports_lists, port_left=0):
        print("Number of connection: {}".format(port_left))
        client_socket.send(str(ports_lists[port_left]).encode())
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((LOCALHOST, ports_lists[port_left]))

        server.listen()
        client, addr = server.accept()
        if (port_left == 9):
            client.send("Here's the flag :)\nEPICTF{1nt3rm3d14ry_1s_4w3s0m3}".encode())
            client.close()
            server.close()
            return
        self._run_another_server(client, ports_lists, port_left + 1)


    def _generate_port(self):
        port = 0
        ports_lists = []
        for i in range(0, 10):
            port = random.randint(10000, 65535)
            if not port in self._ports_list:
                ports_lists.append(port)
        return ports_lists

    def run(self):
        self._server_socket.bind((LOCALHOST, self._port))
        self._server_socket.listen()
        while True:
            print("Waiting for new connections...")
            read_socket, write_socket, exception_socket = select.select([self._server_socket], [], [], 2)
            for socks in read_socket:
                if (socks == self._server_socket):
                    client_socket, client_address = self._server_socket.accept()
                    print("New connection from {}".format(client_address))
                    self._client_lists.append(client_socket)
                    self._ports_list.append(self._generate_port())
                    thread = threading.Thread(target=self._run_another_server, args=(client_socket, self._ports_list[-1]))
                    thread.start()


if __name__ == "__main__":
    server = Server()
    server.run()
