import os
import pyexcel
import csv
from collections import OrderedDict

CLIENT_CACHE_DIR = './client_cache'
OUT_EXAMINATOR_CSV = './client_cache/_examinator.csv'
OUT_ROOM_CSV = './client_cache/_room.csv'

if not os.path.exists(CLIENT_CACHE_DIR):
    os.makedirs(CLIENT_CACHE_DIR)


def convert_examinator(xlsx_file):
    records = pyexcel.get_records(file_name=xlsx_file)
    csv_records = []
    for record in records:
        csv_record: OrderedDict = OrderedDict()
        csv_record["Mã GV"] = record["Mã GV"]
        csv_record["Họ Tên"] = record["Họ Tên"]
        csv_record["Ngày sinh"] = record["Ngày sinh"]
        csv_record["Đơn vị công tác"] = record["Đơn vị công tác"]
        csv_records.append(csv_record)

    pyexcel.save_as(records=csv_records, dest_file_name=OUT_EXAMINATOR_CSV)


def convert_room(xlsx_file):
    records = pyexcel.get_records(file_name=xlsx_file)
    csv_records = []
    for record in records:
        csv_record: OrderedDict = OrderedDict()
        csv_record["Phòng thi"] = record["Phòng thi"]
        csv_record["Địa điểm"] = record["Địa điểm"]
        csv_records.append(csv_record)

    pyexcel.save_as(records=csv_records, dest_file_name=OUT_ROOM_CSV)
