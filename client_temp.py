#!/bin/python3

from socket import socket
import sys

if (len(sys.argv) != 2):
    print("Usage: python3 client_temp.py <PORT>")
    exit(0)

PORT = sys.argv[1]

s = socket()
s.connect(("localhost", int(PORT)))
print("Connected to server")

try:
    for nb in range(10):
        port = s.recv(1024).decode()
        if not port.isdigit():
            print("Error: received port is not a number")
            exit(0)
        port = int(port)
        print("Received port: " + str(port))
        s.close()
        s = socket()
        s.connect(("localhost", port))
        print("Connected to server")
except ConnectionRefusedError:
    print("{} is not available".format(port))
    exit(0)

print(s.recv(1024).decode())
s.close()

