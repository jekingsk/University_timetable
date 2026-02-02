def is_faculty_free(timetable, faculty_id, day, slot):
    for entry in timetable:
        if entry["faculty_id"] == faculty_id and entry["day"] == day and entry["slot"] == slot:
            return False
    return True

def is_room_free(timetable, room_id, day, slot):
    for entry in timetable:
        if entry["room_id"] == room_id and entry["day"] == day and entry["slot"] == slot:
            return False
    return True
def is_room_suitable(room_capacity, class_size):
    if room_capacity is None:
        return False
    return room_capacity >= class_size

