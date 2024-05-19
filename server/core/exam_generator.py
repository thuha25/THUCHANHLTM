import os
from server.data.examinator import Examinator
from server.data.exam_room import ExamRoom
from server.data.order import RoomOrder
import csv
import random

FIRST_CACHE_FILE = 'first'
LAST_CACHE_FILE = 'cache'

room_cache = {}
partner_cache = {}


def check_valid(iter, rooms) -> bool:
    ifirst, ilast = iter
    for id, eid in enumerate(ifirst):
        if id >= len(rooms):
            break
        if room_cache.get(eid) and rooms[id] in room_cache[eid]:
            return False
    for id, eid in enumerate(ilast):
        if id >= len(rooms):
            break
        if room_cache.get(eid) and rooms[id] in room_cache[eid]:
            return False

    for i in range(len(rooms)):
        if partner_cache.get(ifirst[i]) and ilast[i] in partner_cache[ifirst[i]]:
            return False

    return True


def next_iterator():
    exam_rooms = ExamRoom.get_all()
    room_ids = [exam_rooms[i].id for i in range(len(exam_rooms))]
    examinators = Examinator.get_all()
    examinator_ids = [examinators[i].id for i in range(len(examinators))]

    _first_half_examnimators = examinator_ids[:len(examinator_ids)//2]
    _last_half_examnimators = examinator_ids[len(examinator_ids)//2:]

    if not os.path.exists(LAST_CACHE_FILE):
        first_half_examnimators = _first_half_examnimators
        last_half_examnimators = _last_half_examnimators

        if not check_valid((first_half_examnimators, last_half_examnimators), room_ids):
            return None
    else:
        with open(LAST_CACHE_FILE, 'r') as f:
            data = f.read()
            first_str, last_str = data.split('\n')

            first_half_examnimators = first_str.split(',')
            last_half_examnimators = last_str.split(',')

            first_half_examnimators.append(first_half_examnimators[0])
            first_half_examnimators.pop(0)

            last_half_examnimators.append(last_half_examnimators[0])
            last_half_examnimators.append(last_half_examnimators[1])
            last_half_examnimators.pop(0)
            last_half_examnimators.pop(0)

            if not check_valid((first_half_examnimators, last_half_examnimators), room_ids):
                return None

    result = []
    for id, room_id in enumerate(room_ids):
        e1 = first_half_examnimators[id]
        e2 = last_half_examnimators[id]
        record = (room_id, e1, e2)

        if not e1 in partner_cache:
            partner_cache[e1] = [e2]
        else:
            partner_cache[e1].append(e2)

        if not e2 in partner_cache:
            partner_cache[e2] = [e1]
        else:
            partner_cache[e2].append(e1)

        if not e1 in room_cache:
            room_cache[e1] = [room_id]
        else:
            room_cache[e1].append(room_id)

        if not e2 in room_cache:
            room_cache[e2] = [room_id]
        else:
            room_cache[e2].append(room_id)

        result.append(record)

    with open(LAST_CACHE_FILE, 'w') as f:
        f.write(','.join(first_half_examnimators) + '\r')
        f.write(','.join(last_half_examnimators))

    remain_first_half = first_half_examnimators[len(room_ids):]
    remain_last_half = last_half_examnimators[len(room_ids):]

    return result, remain_first_half, remain_last_half


OUT_ROOM_CSV = './server/out_room.csv'
OUT_REMAIN_CSV = './server/out_remain.csv'


def generate() -> bool:
    result = next_iterator()
    if (result == None):
        return False
    results, remain1, remain2 = result
    id = 0

    orders = []
    for result in results:
        examinator1 = Examinator.get(result[1])
        examinator2 = Examinator.get(result[2])

        order1 = RoomOrder(id, examinator1, True, result[0])
        order2 = RoomOrder(id + 1, examinator2, False, result[0])

        id += 2

        orders.append(order1)
        orders.append(order2)

    with open(OUT_ROOM_CSV, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel', lineterminator='\r')
        headers = ['STT', 'Mã GV', 'Họ và tên',
                   'Giám thị 1', 'Giám thị 2', 'Phòng thi']
        writer.writerow(headers)
        for order in orders:
            writer.writerow(order.to_record())

    remain = [*remain1, *remain2]
    exam_rooms = ExamRoom.get_all()

    current = 0

    with open(OUT_REMAIN_CSV, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel', lineterminator='\r')
        headers = ['STT', 'Mã GV', 'Họ và tên', 'Phòng thi được giám sát']
        writer.writerow(headers)
        c = 0
        while True:
            c += 1
            num = random.randint(2, 8)
            last = min(current + num, len(exam_rooms)) - 1
            room = f"Từ {exam_rooms[current].id} đến {exam_rooms[last].id}"
            current += num
            writer.writerow(
                [c, remain[c - 1], Examinator.get(remain[c - 1]).name, room])
            if current >= len(exam_rooms):
                break

    return True


def clear_cache():
    global room_cache
    global partner_cache
    room_cache = {}
    partner_cache = {}
    if os.path.exists(LAST_CACHE_FILE):
        os.remove(LAST_CACHE_FILE)
