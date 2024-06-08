import os
import socket
import tqdm
import rsa
from Crypto.Cipher import AES

def createSocket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client

def generateKey():
    #-->Generating a random key and nonce using os
    key = os.urandom(16)
    nonce = os.urandom(16)
    return key, nonce

def send_key_and_nonce(client, key, nonce):
    #--> sending encrypted message using the public key sent by the server 
    #1)Receiving the public key:
    public_key = client.recv(256)
    publicKey = rsa.PublicKey.load_pkcs1(public_key)
    #2)encrypting key and nonce:
    encryptedKey = rsa.encrypt(key, publicKey)
    encryptedNonce = rsa.encrypt(nonce, publicKey)
    #3)sending encrypted key and nonce:
    client.send(encryptedKey)
    client.send(encryptedNonce)

def main():
    key, nonce = generateKey()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    host=input("Enter the IP address:")
    port=int(input("Enter port:"))

    client = createSocket()
    client.connect((host, port))
    send_key_and_nonce(client, key, nonce)

    fileName = input("Enter the file name including the format: ")
    file_size = os.path.getsize(fileName)

    client.send(fileName.encode('ascii'))
    client.send(str(file_size).encode('ascii'))

    progress = tqdm.tqdm(range(file_size), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(fileName, "rb") as file:
        while True:
            bytes_read = file.read(1024)
            if not bytes_read:
                break
            encrypted_data = cipher.encrypt(bytes_read)
            client.sendall(encrypted_data)
            progress.update(len(bytes_read))

    client.send(b"<END>")
    print("File sent successfully")
    client.close()

if __name__ == "__main__":
    main()
