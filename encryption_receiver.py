import socket
import tqdm
import rsa
import os
from Crypto.Cipher import AES

def createSocket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server

def createKeys():
    # Generating public key and private key using rsa
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key

def send_and_receive(public_key, private_key, client):
    #--> Here the public key is sent to the client and client will encrypt the message   using this public key
    publicKey = public_key.save_pkcs1()
    client.send(publicKey)
    #--> The encrypted message is being received and by using the private key one        can decrypt the message
    key = rsa.decrypt(client.recv(256), private_key)  # Adjusted for RSA 1024-bit
    nonce = rsa.decrypt(client.recv(256), private_key)
    return key, nonce

def main():
    host=input("Enter the IP address:")
    port=int(input("Enter port:"))
    server = createSocket()
    server.bind((host, port))
    server.listen()
    print(f"Server listening on port {port}...")
    client, address = server.accept()
    print(f"Connected to {address}")

    public_key, private_key = createKeys()
    key, nonce = send_and_receive(public_key, private_key, client)

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    file_name = client.recv(1024).decode('ascii')
    file_size = int(client.recv(1024).decode('ascii'))
    print(f"Receiving {file_name} of size {file_size} bytes")

    progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1024, total=file_size)
    file_byte = b""

    while True:
        data = client.recv(1024)
        if data[-5:] == b"<END>":
            file_byte += data[:-5]
            progress.update(len(data) - 5)
            break
        file_byte += data
        progress.update(len(data))

    decrypted_data = cipher.decrypt(file_byte)

    # Save the received file with a different name to avoid conflicts
    received_file_name = "received_" + file_name
    with open(received_file_name, "wb") as file:
        file.write(decrypted_data)

    print(f"File received and decrypted successfully as {received_file_name}")
    server.close()
    client.close()

if __name__ == "__main__":
    main()
