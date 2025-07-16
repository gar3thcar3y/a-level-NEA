import Connections
import time

clients = Connections.get_clients(1)

for i in range(1000):
    for client in clients:
        print(client.getdata())
        time.sleep(3)