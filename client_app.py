from tkinter import *
from tkinter import filedialog, messagebox
import socket
import pyexcel
import os
from util.fileio import receive_file

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8000))


def select_file_1():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        label_file_1.config(text=file_path)


def select_file_2():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        label_file_2.config(text=file_path)


def add_command():
    with open(label_file_1.cget("text"), "rb") as f:
        data = f.read()
        msg = f"set_examinator {len(data)}"
        client.send(msg.encode())
        msg = client.recv(1024).decode()
        if msg == "ready":
            client.send(data)
            msg = client.recv(1024).decode()
            if msg == "done":
                print("Examinator file received")

    with open(label_file_2.cget("text"), "rb") as f:
        data = f.read()
        msg = f"set_room {len(data)}"
        client.send(msg.encode())
        msg = client.recv(1024).decode()
        if msg == "ready":
            client.send(data)
            msg = client.recv(1024).decode()
            if msg == "done":
                print("Room file received")

    client.send(b"generate")
    msg = client.recv(1024).decode().split()
    if len(msg) == 2:
        msg, size = msg[0], int(msg[1])

        if msg == "file_ready":
            client.send(b"ready")
            receive_file(client, "out_room.csv", size)
            print("Room file received")
            client.send(b"done")

            sheet = pyexcel.get_sheet(file_name="out_room.csv", delimiter=",")
            sheet.save_as("DanhSachPhanCong.xlsx")

            msg = client.recv(1024).decode().split()
            if len(msg) == 2:
                msg, size = msg[0], int(msg[1])

                if msg == "file_ready":
                    client.send(b"ready")
                    receive_file(client, "out_remain.csv", size)
                    print("Room file received")
                    client.send(b"done")

                    sheet = pyexcel.get_sheet(
                        file_name="out_remain.csv", delimiter=",")
                    sheet.save_as("DanhSachGiamSat.xlsx")

                    # Open the new window with the buttons
                    open_result_window()
            else:
                print("Error")
        else:
            print("Error")


def open_file(file_path):
    try:
        os.startfile(file_path)  # Windows
    except AttributeError:
        try:
            subprocess.call(['open', file_path])  # Mac
        except:
            subprocess.call(['xdg-open', file_path])  # Linux


def open_result_window():
    result_window = Toplevel(root)
    result_window.geometry("400x200")
    result_window.configure(bg="#f0f0f0")
    result_window.title("Generated Files")

    btn_view_phancong = Button(result_window, text="Xem DanhSachPhanCong.xlsx", bg="#4CAF50", fg="white",
                               font=('Helvetica', 12), relief=FLAT, command=lambda: open_file("DanhSachPhanCong.xlsx"))
    btn_view_phancong.pack(pady=20)

    btn_view_giamsat = Button(result_window, text="Xem DanhSachGiamSat.xlsx", bg="#4CAF50", fg="white",
                              font=('Helvetica', 12), relief=FLAT, command=lambda: open_file("DanhSachGiamSat.xlsx"))
    btn_view_giamsat.pack(pady=20)


root = Tk()
root.geometry("600x400")
root.configure(bg="#f0f0f0")

w = Label(root, text='Phân công cán bộ coi thi', font=(
    'Helvetica', 16), bg="#f0f0f0", fg="#333333")
w.pack(pady=20)

btn_file_1 = Button(root, text="Chọn Giám Thị Coi Thi CSV",
                    bg="#4CAF50", fg="white", font=('Helvetica', 12), relief=FLAT, command=select_file_1)
btn_file_1.pack(pady=10)

label_file_1 = Label(root, text="Chưa chọn file",
                     bg="#f0f0f0", fg="#333333", font=('Helvetica', 12))
label_file_1.pack(pady=5)

btn_file_2 = Button(root, text="Chọn Phòng Thi CSV",
                    bg="#4CAF50", fg="white", font=('Helvetica', 12), relief=FLAT, command=select_file_2)
btn_file_2.pack(pady=10)

label_file_2 = Label(root, text="Chưa chọn file",
                     bg="#f0f0f0", fg="#333333", font=('Helvetica', 12))
label_file_2.pack(pady=5)

btn_add = Button(root, text="Add", bg="#2196F3", fg="white", font=(
    'Helvetica', 12), relief=FLAT, command=add_command)
btn_add.pack(pady=20)

root.mainloop()
