#!/bin/python3

from socket import socket
import sys

if (len(sys.argv) != 2):
    print("Usage: python3 client_temp.py <PORT>")
    exit(0)

PORT = sys.argv[1]

s = socket()
s.connect(("localhost", int(PORT)))

while True:
    msg = input("Enter message: ")
    s.send(msg.encode())
    if msg == "exit":
        break
    print("Message sent.")

s.close()

