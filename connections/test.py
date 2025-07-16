import socket

print("Creating server...")
s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 10000))

print(socket.gethostbyname(socket.gethostname()))

s.listen(0)

client, addr = s.accept()
print("[esp32 connected]")


while True:
        content = client.recv(32)
        if len(content) == 0:
                break
        else:
                print(content)
print("Closing connection")
client.close()