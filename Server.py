# Made by Alisher Sultanov and Ablan Abkenov

import socket
import time
import json
import pickle
import _thread

file_info = {}
active_clients = []

def serve(clientsocket,addr):
    client_ip, client_port = clientsocket.getsockname()
    addr = [addr[0], addr[1]]

    while True:
        #print("Got a connection from %s" % str(addr))
        try:
            msg = clientsocket.recv(1024).decode("utf-8")
        except:
            pass
        if len(msg) > 0:
            if (msg != "HELLO"):
                print(msg[0:8])

            if (msg == 'HELLO'):
                clientsocket.send(b'HI')
                recv_data = b''
                recv_data += clientsocket.recv(1024)
                info = pickle.loads(recv_data)

                if len(info) > 0:
                    for file in info:
                        if file[0] in file_info:
                            file_info[file[0]].append(file)
                        else:
                            file_info[file[0]] = [file]
                        client_info = [file[len(file) - 2], file[len(file) - 1]]
                        if client_info not in active_clients:
                            active_clients.append(client_info)
                    print(file_info)
                else:
                    active_clients.remove(addr)
                    clientsocket.close()
                msg = ""

            elif (msg[0:8] == "SEARCH: "):
                title = msg[8:]
                arr = []
                #print(title)
                #print(file_info)
                if title in file_info:
                    for inf in file_info[title]:
                        client = [inf[len(inf) - 2],inf[len(inf) - 1]]
                        if client in active_clients and (client[0] != addr[0] or client[1] != addr[1]):
                                arr.append(inf)
                data = pickle.dumps(arr)
                clientsocket.send(data)
                #else:
                    #active_clients.remove(addr)
                    #clientsocket.close()
                msg = ""

            elif (msg =="CLOSE"):
                active_clients.remove(addr)
                clientsocket.close()
                msg = ""


# create a socket object
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
ip = socket.gethostbyname(host)

port = 9999

# bind to the port
serversocket.bind((host, port))

print(ip + " " + str(port))
# queue up to 5 requests
serversocket.listen(5)

# establish a connection




while True:

    clientsocket, addr = serversocket.accept()

    _thread.start_new_thread(serve, (clientsocket, addr))











