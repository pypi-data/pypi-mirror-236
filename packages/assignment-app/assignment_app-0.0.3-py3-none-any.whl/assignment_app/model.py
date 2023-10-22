import datetime


class Assignment:
    def __init__(
        self,
        assignment,
        course,
        date_due,
        date_added=None,
        date_completed=None,
        status=None,
        position=None,
    ):
        self.assignment = assignment
        self.course = course
        self.date_due = date_due
        self.date_added = (
            date_added
            if date_added is not None
            else datetime.datetime.now().isoformat()
        )
        self.date_completed = date_completed if date_completed is not None else None
        self.status = (
            status if status is not None else 1
        )  # 1 = incomplete, 2 = completed
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return (
            f"Assignment: {self.assignment} | Course: {self.course} "
            + f" | Date_Due: {self.date_due} | Date Added: {self.date_added} "
            + f" | Date Completed: {self.date_completed} "
            + f" | Satus: {self.status} | Position: {self.position}"
        )
