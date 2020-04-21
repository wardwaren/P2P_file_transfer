# Made by Alisher Sultanov and Ablan Abkenov

import socket
import tkinter as tk
import pickle
import _thread
import time
import datetime
from tkinter import filedialog
from os import scandir
from pathlib import Path
from tkinter import messagebox




folder = ""


def serve(clientsocket,addr):
    while True:
        #print("Got a connection from %s" % str(addr))
        try:
            msg = clientsocket.recv(1024).decode("utf-8")
        except:
            pass
        if len(msg) > 0:
            if (msg != "HELLO"):
                print(msg[0:8])

            if (msg[0:8] == 'DOWNLOAD'):
                recv_data = b''
                recv_data += clientsocket.recv(1024)
                data = pickle.loads(recv_data)
                file_name = data[0]
                file_name += data[1]
                f = open(window.directory + "/" + file_name, 'rb')
                l = f.read(1024)
                while (l):
                    clientsocket.send(l)
                    l = f.read(1024)
                    if(l == 0):
                        break
                f.close()


def listen():
    while True:
        try:
            # create a socket object
            serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

            # get local machine name
            host = socket.gethostname()

            # bind to the port
            serversocket.bind((host, window.get_port()))

            # queue up to 5 requests
            serversocket.listen(5)

            # establish a connection

            while True:
                clientsocket, addr = serversocket.accept()
                _thread.start_new_thread(serve, (clientsocket, addr))
            # print("The time got from the server is %s" % tm.decode('ascii'))
        except:
            pass



class Client(tk.Tk):
    def __init__(self):
        _thread.start_new_thread(listen,())
        # create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        self.host = socket.gethostname()



        # create files in the client
        self.directory = ""
        self.files = []
        self.search_results = []

        tk.Tk.__init__(self)
        self.create_title("You are using client version \n Please enter server ip and server port (Custom port 9999) \n"
                          "Also select folder from which copy and to which download" )
        # create an input
        self.host = tk.Entry(fg="#dd4814", bg="black", width=50)
        self.host.pack()
        # create an input
        self.port = tk.Entry(fg="#dd4814", bg="black", width=50)
        self.port.pack()
        # create a button
        self.button_connect = tk.Button(
            text="Connect",
            width=25,
            height=5,
            bg="black",
            fg="#dd4814",
            command=self.connect_to_server
        )
        self.button_upload = tk.Button(text='Open',
            width=25,
            height=5,
            bg="black",
            fg="#dd4814", command=self.get_folder)
        self.button_upload.pack()
        self.button_connect.pack(side='bottom')



    def connect_to_server(self):

        if self.directory == "":
            self.greeting['text'] = "Please choose folder first"

        elif self.host.get() != "" and self.port.get() != "":
            #192.168.0.159
            self.host = self.host.get()
            port = int(self.port.get())
            #try:
            # connection to hostname on the port.
            self.s.connect((self.host, port))
            self.ip, self.port = self.s.getsockname()
            for i in self.files:
                i.append(self.ip)
                i.append(self.port)

            self.s.sendall(b'HELLO')
            # Receive no more than 1024 bytes
            msg = self.s.recv(1024).decode("utf-8")
            if msg == 'HI':
                self.send_info(self.files)
                self.clean_window()
                self.create_title("Succesfully connected \n Enter file to search")
                self.send_info(self.files)
                self.entry = tk.Entry(fg="#dd4814", bg="black", width=50)
                self.entry.pack()
                self.button_upload = tk.Button(text='Find',
                                               width=25,
                                               height=5,
                                               bg="black",
                                               fg="#dd4814", command=self.find_file)
                self.button_upload.pack()
                self.button_upload.pack(side='bottom')


            else:
                self.greeting['text'] = "Strange response from the server"

            #except:
            #    print("Couldn't connect to the server")

            #self.s.close()
        else:
            self.greeting['text'] = "Type into input!"

    def find_file(self):
        self.greeting["text"] = "Succesfully connected \n Enter file to search"
        file_title = self.entry.get()
        self.s.sendall(('SEARCH: ' + file_title).encode())
        recv_data = b''
        recv_data += self.s.recv(1024)
        data = pickle.loads(recv_data)

        if(len(data) == 0):
            self.greeting["text"] = "File doesn't exist"
        else:
            self.search_results = data
            self.clean_window()
            self.create_title("These are found files \n Enter FileName,type,size to download")
            for i in range(len(self.search_results)):
                info = str(i) + ") "
                for data in self.search_results[i]:
                    info += str(data) + " "
                self.create_query(info)
            self.entry = tk.Entry(fg="#dd4814", bg="black", width=50)
            self.entry.pack()
            self.button_upload = tk.Button(text='Select',
                                           width=25,
                                           height=5,
                                           bg="black",
                                           fg="#dd4814", command=self.select_file)
            self.button_upload.pack()
            self.button_upload.pack(side='bottom')


    def select_file(self):
        file = self.search_results[int(self.entry.get())]
        self.clean_window()
        data = pickle.dumps(file)
        self.s.close()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, file[len(file) - 1]))
        self.create_title("You are now downloading from other user")
        self.s.sendall(b'DOWNLOAD:')
        self.s.sendall(data)
        with open(self.directory + "/" + file[0] + file[1], 'wb') as f:
            while True:
                data = self.s.recv(1024)
                print(data)
                if len(data) < 1024:
                    f.write(data)
                    break
                # write data to a file
                f.write(data)
            f.close()



    def clean_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_title(self,msg):

        self.greeting = tk.Label(text=msg, bg="black",
                                 fg="#dd4814",
                                 width=80, height=5)
        self.greeting.config(font=("Courier", 24))
        self.greeting.pack()

    def create_query(self,msg):
        self.greeting = tk.Label(text=msg, bg="black",
                                 fg="#dd4814",
                                 width= 80, height=2)
        self.greeting.config(font=("Courier", 12))
        self.greeting.pack()

    def send_info(self,files):
        #js = json.dumps(self.files).encode('utf-8')
        data = pickle.dumps(files)
        self.s.sendall(data)

    def get_folder(self):
        dir = filedialog.askdirectory()
        self.directory = dir
        #self.files = [f for f in scandir(dir) if isfile(join(dir, f.stat()))]
        folder = dir
        for f in scandir(dir):
            filename = dir + "/" + f.name
            mod_time = datetime.datetime.strptime(time.ctime(f.stat().st_mtime),"%a %b %d %H:%M:%S %Y")
            if mod_time.month < 10:
                month = "0" + str(mod_time.month)
            else:
                month = str(mod_time.month)
            if mod_time.day < 10:
                day = "0" + str(mod_time.day)
            else:
                day = str(mod_time.day)

            mod_time = day + "/" + month + "/" + str(mod_time.year)

            info = [Path(filename).stem, Path(filename).suffix, f.stat().st_size, mod_time]
            self.files.append(info)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.s.sendall((b'CLOSE'))
            except:
                pass
            self.destroy()

    def get_port(self):
        return self.port

    def get_socket(self):
        return self.s








window = Client()

window.protocol("WM_DELETE_WINDOW", window.on_closing)
window.mainloop()

