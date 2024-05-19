import socket


def receive_file(client: socket.socket, filename: str, content_length: int):
    byte_read = 0
    with open(filename, "wb") as file:
        file_content = client.recv(min([1024, content_length - byte_read]))
        byte_read += len(file_content)
        while (byte_read < content_length):
            file.write(file_content)
            file_content = client.recv(min([1024, content_length - byte_read]))
            byte_read += len(file_content)
        if file_content:
            file.write(file_content)
