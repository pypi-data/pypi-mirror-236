import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from dacite import from_dict
from rich.prompt import Confirm, Prompt
from typing_extensions import Annotated

from . import __version__
from .console import console
from .constants import (
    DATE_FORMAT,
    KETTLEBELLS_DB,
    KETTLEBELLS_HOME,
    WARNING,
)
from .database import (
    cache_workout,
    confirm_loads,
    initialize_database,
    read_database,
    save_workout,
    write_database,
)
from .stats import get_all_time_stats, plot_workouts, top_ten_workouts
from .workouts import (
    Workout,
    create_btb_workout,
    create_ic_or_abc,
    create_custom_workout,
    random_ic_or_abc,
    set_loads,
)

cli = typer.Typer(add_completion=False)


def report_version(display: bool) -> None:
    """Print version and exit."""
    if display:
        console.print(f"{Path(sys.argv[0]).name} {__version__}")
        raise typer.Exit()


@cli.callback()
def global_options(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        is_flag=True,
        is_eager=True,
        callback=report_version,
    ),
):
    """Create, save, and track progress of kettlebell workouts."""


@cli.command()
def init(
    ctx: typer.Context,
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        is_flag=True,
        is_eager=True,
    ),
) -> None:
    """Initializes the kettlebells database."""
    initialize_database(
        kettlebells_home=KETTLEBELLS_HOME,
        db_path=KETTLEBELLS_DB,
        force=force,
    )


@cli.command()
def setloads(ctx: typer.Context) -> None:
    """Set units and loads for workouts."""
    loads = set_loads()
    data = read_database(KETTLEBELLS_DB)
    data["loads"] = loads
    write_database(KETTLEBELLS_DB, data)


@cli.command()
def workout(
    ctx: typer.Context,
    workout_type: Annotated[
        str, typer.Argument(help="Possible workouts are ic or abc")
    ],
) -> None:
    """Create a random iron cardio or armor building complex workout."""
    confirm_loads(KETTLEBELLS_DB)
    workout = random_ic_or_abc(KETTLEBELLS_DB, workout_type)
    cache_workout(KETTLEBELLS_DB, workout)
    workout.display_workout()


@cli.command()
def done(
    ctx: typer.Context,
    workout_type: Annotated[
        Optional[str],
        typer.Argument(help="Possible workouts are ic, abc, or btb."),
    ] = None,
) -> None:
    """Save a kettlebell workout.

    If no argument is passed, kettlebells will attempt to use the most recently generated workout.
    """
    confirm_loads(KETTLEBELLS_DB)
    data = read_database(KETTLEBELLS_DB)
    match workout_type:
        case "ic" | "abc":
            workout = create_ic_or_abc(KETTLEBELLS_DB, workout_type)
        case "btb":
            workout = create_btb_workout(KETTLEBELLS_DB)
        case "custom":
            workout = create_custom_workout(KETTLEBELLS_DB)
        case _:
            workout = from_dict(Workout, data["cached_workouts"][-1])
            console.print("Last workout generated:\n")
    workout.display_workout()
    if Confirm.ask("Save this workout?"):
        workout_date = _get_date()
        save_workout(KETTLEBELLS_DB, workout_date, workout)
        print()
        workout.display_workout_stats()
    else:
        console.print("Workout not saved.")


@cli.command()
def last(ctx: typer.Context) -> None:
    """Display stats from most recent workout in database."""
    data = read_database(KETTLEBELLS_DB)
    last_workout = data["saved_workouts"][-1]
    workout_date = last_workout["date"]
    workout = from_dict(Workout, last_workout["workout"])
    console.print(
        f"\nDate: [green]{datetime.strptime(workout_date, DATE_FORMAT):%b %d, %Y}\n"
    )
    workout.display_workout()
    print()
    workout.display_workout_stats()


@cli.command()
def stats(
    ctx: typer.Context,
    plot: bool = typer.Option(
        False,
        "--plot",
        "-p",
        is_flag=True,
        is_eager=True,
    ),
) -> None:
    """Display stats from all workouts in database."""
    data = read_database(KETTLEBELLS_DB)
    dates, weight_per_workout = get_all_time_stats(data)
    if plot:
        plot_workouts(dates, weight_per_workout)


@cli.command()
def best(
    ctx: typer.Context,
    sort: Annotated[
        str,
        typer.Option(
            "--sort",
            "-s",
            help="Sort the table. Possible arguments: weight moved, reps, density.",
        ),
    ] = "weight-moved",
) -> None:
    """Display a table of the top ten workouts in database."""
    data = read_database(KETTLEBELLS_DB)
    console.print(top_ten_workouts(data, sort))


def _get_date() -> str:
    """A helper function to get the date of a workout.

    Returns:
        A str of the date formatted as YYYY-MM-DD.
    """
    while True:
        workout_date = Prompt.ask(
            "Enter the date of the workout (YYYY-MM-DD), or press enter for today"
        )
        if not workout_date:
            workout_date = datetime.now().strftime(DATE_FORMAT)
        try:
            datetime.strptime(workout_date, DATE_FORMAT)
            break
        except ValueError:
            console.print(":warning: {workout_date} not a valid date.", style=WARNING)
            continue
    return workout_date


if __name__ == "__main__":
    cli()
