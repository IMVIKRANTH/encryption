import os
import socket

port=9090
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",port))

file=open("image.png","rb")
file_size=os.path.getsize("image.png")

client.send("received_image.png".encode())
client.send(str(file_size).encode())

data=file.read()
client.sendall(data)
client.send(b"{END}")

file.close()
client.close()
