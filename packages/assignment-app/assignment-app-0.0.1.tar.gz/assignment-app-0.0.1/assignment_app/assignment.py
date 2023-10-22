import typer
from rich.console import Console
from rich.table import Table
from model import Assignment
from query import (
    get_all_assignment,
    delete_assignment,
    insert_assignment,
    complete_assignment,
    update_assignment,
)

console = Console()

app = typer.Typer()

# @app.group()
# @app.option("--help", default="---help", help="Display user guide")
@app.command(short_help="adds an assignment, course code, and due date")
def add(
    assignment: str = typer.Option(..., prompt=True),
    course: str = typer.Option(..., prompt=True),
    date_due: str = typer.Option(..., prompt=True),
):
    typer.echo(f"adding {assignment}, {course}, {date_due}")
    assignment = Assignment(assignment, course, date_due)
    insert_assignment(assignment)
    show()


@app.command(short_help="deletes an assignmnet at specified position")
def delete(position: int = typer.Option(..., prompt=True)):
    typer.echo(f"deleting assignment at position: {position}")
    # indices in CLI begin at 1, but in database at 0
    delete_assignment(position - 1)
    show()


@app.command(short_help="updates an assignment at specified position")
def update(
    position: int = typer.Option(..., prompt=True),
    assignment: str = typer.Option(..., prompt=True),
    course: str = typer.Option(..., prompt=True),
    date_due: str = typer.Option(..., prompt=True),
):
    typer.echo(f"updating assignment at position: {position}")
    update_assignment(position - 1, assignment, course, date_due)
    show()


@app.command(short_help="completes an assignment at specified position")
def complete(position: int = typer.Option(..., prompt=True)):
    typer.echo(f"completing assignment at position: {position}")
    complete_assignment(position - 1)
    show()


@app.command(short_help="shows all assignments")
def show():
    assignment = get_all_assignment()
    console.print("[bold magenta]Assignment[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Assignment", min_width=20)
    table.add_column("Course", min_width=12, justify="right")
    table.add_column("Date Due", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_course_color(course):
        COLORS = {
            "IDS 702": "blue",
            "IDS 720": "red",
            "IDS 703": "yellow",
            "IDS 706": "green",
        }
        if course in COLORS:
            return COLORS[course]
        return "white"

    for idx, assignment in enumerate(assignment, start=1):
        c = get_course_color(assignment.course)
        is_done_str = "✅" if assignment.status == 2 else "❌"
        table.add_row(
            str(idx),
            assignment.assignment,
            f"[{c}]{assignment.course}[/{c}]",
            assignment.date_due,
            is_done_str,
        )
    console.print(table)
    print(assignment)
    return "Success!"


if __name__ == "__main__":
    app()
