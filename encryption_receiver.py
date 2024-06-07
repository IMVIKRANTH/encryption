import socket
import os 

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",9090))
server.listen()

client ,address=server.accept()

file_name=client.recv(1024).decode()
print(file_name)
file_size=client.recv(1024).decode()
print(file_size)

file = open(file_name,"wb")
file_byte=b""
oper=False

#progress= tqdm.tqdm(unit="B",unit_scale=True,unit_divisor=1000,total=int(file_size))

while not oper:
    data=client.recv(1024)
    if file_byte[-5:]==b"{END}":
        done= True
    else:
        file_byte +=data
    #progress.update(1024)

file.write(file_byte)
file.close()
server.close()
client.close()