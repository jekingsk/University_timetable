from engine.constraints import (
    is_faculty_free,
    is_room_free,
    is_room_suitable
)

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
SLOTS = ["9-10", "10-11", "11-12", "1-2", "2-3"]

def generate(classes, subjects, rooms):
    timetable = []

    # Sort classes by size (bigger first)
    classes = sorted(classes, key=lambda c: c["student_count"], reverse=True)

    for cls in classes:
        daily_count = {day: 0 for day in DAYS}

        for subject in subjects:
            for _ in range(subject["weekly_hours"]):
                assigned = False

                for day in DAYS:
                    # Enforce at least one free hour per day
                    if daily_count[day] >= len(SLOTS) - 1:
                        continue

                    for slot in SLOTS:
                        for room in rooms:
                            if not is_room_suitable(room["capacity"], cls["student_count"]):
                                continue

                            if (
                                is_faculty_free(timetable, subject["faculty_id"], day, slot)
                                and is_room_free(timetable, room["id"], day, slot)
                                and not any(
                                    t["class_id"] == cls["id"]
                                    and t["day"] == day
                                    and t["slot"] == slot
                                    for t in timetable
                                )
                            ):
                                timetable.append({
                                    "class_id": cls["id"],
                                    "subject_id": subject["id"],
                                    "faculty_id": subject["faculty_id"],
                                    "room_id": room["id"],
                                    "day": day,
                                    "slot": slot
                                })
                                daily_count[day] += 1
                                assigned = True
                                break

                        if assigned:
                            break
                    if assigned:
                        break

    return timetable
