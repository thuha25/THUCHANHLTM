import socket
from tkinter import *
import threading
import logger
from server.server import Server
from server.core import exam_generator
import server.importdb as importdb
from util.fileio import receive_file

app = Tk()

app.title("Server")

log = Text(app, state='disabled')

logger.register_callback(lambda msg: log.configure(state='normal') or log.insert(
    'end', msg + '\n') or log.configure(state='disabled'))

scroll = Scrollbar(app, orient='vertical', command=log.yview)
log.configure(yscrollcommand=scroll.set)

scroll.pack(side='right', fill='y')
log.pack(side='left', fill='both', expand=True)


def start_server():
    server = Server(handler=client_handler)
    server.start()


def client_handler(server: Server, client: socket.socket, addr):
    while True:
        commands = client.recv(1024).decode().split()
        if not commands:
            continue
        command = commands[0]
        if not command:
            break
        logger.log(f"Received command: {command} from {addr}")
        if command == "exit":
            break
        if command == "set_examinator":
            size = int(commands[1])
            client.send(b"ready")
            logger.log("Receiving examinator file")
            receive_file(client, "_CanBoCoiThi.csv", size)
            logger.log("Examinator file received")
            importdb .import_examinators("_CanBoCoiThi.csv")
            logger.log("Examinator file received")
            client.send(b"done")

        if command == "set_room":
            size = int(commands[1])
            client.send(b"ready")
            logger.log("Receiving room file")
            receive_file(client, "_room.csv", size)
            importdb .import_rooms("_room.csv")
            logger.log("Room file received")
            client.send(b"done")

        if command == "generate":
            logger.log("Generating exam")

            res = exam_generator.generate()
            if (res):
                with open(exam_generator.OUT_ROOM_CSV, "rb") as file:
                    data = file.read()
                    msg = f"file_ready {len(data)}"
                    client.send(msg.encode())
                    msg = client.recv(1024).decode()
                    if msg == "ready":
                        client.send(data)
                        msg = client.recv(1024).decode()
                        if msg == "done":
                            logger.log("Room file sent")

                with open(exam_generator.OUT_REMAIN_CSV, "rb") as file:
                    data = file.read()
                    msg = f"file_ready {len(data)}"
                    client.send(msg.encode())
                    msg = client.recv(1024).decode()
                    if msg == "ready":
                        client.send(data)
                        msg = client.recv(1024).decode()
                        if msg == "done":
                            logger.log("Remain file sent")

                # msg = client.recv(1024).decode()
                # if msg == "ready":
                #     with open(exam_sorter.OUT_REMAIN_CSV, "rb") as file:
                #         client.sendfile(file)
            else:
                client.send(b"no_file")


threading.Thread(target=start_server).start()

app.mainloop()
