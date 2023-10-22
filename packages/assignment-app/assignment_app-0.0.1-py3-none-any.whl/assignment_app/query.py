import sqlite3
from typing import List
import datetime
from model import Assignment

conn = sqlite3.connect("assignment.db")
c = conn.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXISTS assignment (
            assignment text,
            course text,
            date_due text,
            date_added text,
            date_completed text,
            status integer,
            position integer
            )"""
    )


create_table()


def insert_assignment(assignment: Assignment):
    c.execute("select count(*) FROM assignment")
    count = c.fetchone()[0]
    assignment.position = count if count else 0
    with conn:
        c.execute(
            "INSERT INTO assignment VALUES (:assignment, :course, :date_due, :date_added, :date_completed, :status, :position)",
            {
                "assignment": assignment.assignment,
                "course": assignment.course,
                "date_due": assignment.date_due,
                "date_added": assignment.date_added,
                "date_completed": assignment.date_completed,
                "status": assignment.status,
                "position": assignment.position,
            },
        )


def get_all_assignment() -> List[Assignment]:
    c.execute("select * from assignment")
    results = c.fetchall()
    assignment = []
    for result in results:
        assignment.append(Assignment(*result))
    return assignment


def delete_assignment(position):
    c.execute("select count(*) from assignment")
    count = c.fetchone()[0]

    with conn:
        c.execute(
            "DELETE from assignment WHERE position=:position", {"position": position}
        )
        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)


def change_position(old_position: int, new_position: int, commit=True):
    c.execute(
        "UPDATE assignment SET position = :position_new WHERE position = :position_old",
        {"position_old": old_position, "position_new": new_position},
    )
    if commit:
        conn.commit()


def update_assignment(position: int, assignment: str, course: str, date_due: str):
    with conn:
        if assignment is not None and course is not None and date_due is not None:
            c.execute(
                "UPDATE assignment SET assignment = :assignment, course = :course, date_due = :date_due WHERE position = :position",
                {
                    "position": position,
                    "assignment": assignment,
                    "course": course,
                    "due_date": date_due,
                },
            )
        elif assignment is not None:
            c.execute(
                "UPDATE assignment SET assignment = :assignment WHERE position = :position",
                {"position": position, "assignment": assignment},
            )
        elif course is not None:
            c.execute(
                "UPDATE assignment SET course = :course WHERE position = :position",
                {"position": position, "course": course},
            )
        elif date_due is not None:
            c.execute(
                "UPDATE assignment SET date_due = :date_due WHERE position = :position",
                {"position": position, "date_due": date_due},
            )


def complete_assignment(position: int):
    with conn:
        c.execute(
            "UPDATE assignment SET status = 2, date_completed = :date_completed WHERE position = :position",
            {
                "position": position,
                "date_completed": datetime.datetime.now().isoformat(),
            },
        )
