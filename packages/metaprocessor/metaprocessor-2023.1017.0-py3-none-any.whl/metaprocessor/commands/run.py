import pathlib
from concurrent.futures.thread import ThreadPoolExecutor

import click
from rich import print

import metaprocessor.helpers.config
import metaprocessor.helpers.workflow


@click.group()
def run() -> None:
    """
    Run MetaProcessor workflow.
    """
    pass


@run.command()
@click.option(
    "--key",
    required=False,
    help="Key of the session to be processed.",
)
def preprocess(key: str) -> None:
    """
    Preprocess raw IMU data.
    """
    config = metaprocessor.helpers.config.read()

    if key:
        tasks = [ pathlib.Path(config["general"]["gd-location"])/key ]
    else:
        tasks = metaprocessor.helpers.workflow.generate_tasks(config)

    for task in tasks:
        if not task.exists():
            print(f"[red]Provided session file [u]{task}[/u] does not exist.[/red]")
            raise SystemExit(1)

    print(f"[green]Preprocessing {len(tasks)} session(s).[/green]")

    with ThreadPoolExecutor() as executor:
        executor.map(
            metaprocessor.helpers.workflow.preprocess,
            tasks,
            [config]*len(tasks),
        )


@run.command()
@click.option(
    "--key",
    required=False,
    help="Key of the session to be processed.",
)
def uptime(key: str) -> None:
    """
    Calculate uptime.
    """
    config = metaprocessor.helpers.config.read()

    if key:
        tasks = [ pathlib.Path(config["general"]["gd-location"])/key ]
    else:
        tasks = metaprocessor.helpers.workflow.generate_tasks(config)

    for task in tasks:
        if not task.exists():
            print(f"[red]Provided session file [u]{task}[/u] does not exist.[/red]")
            raise SystemExit(1)

    print(f"[green]Calculating uptime for {len(tasks)} session(s).[/green]")

    with ThreadPoolExecutor() as executor:
        executor.map(
            metaprocessor.helpers.workflow.uptime,
            tasks,
            [config]*len(tasks),
        )


@run.command()
@click.option(
    "--key",
    required=False,
    help="Key of the session to be processed.",
)
def steps(key: str) -> None:
    """
    Calculate steps.
    """
    config = metaprocessor.helpers.config.read()

    if key:
        tasks = [ pathlib.Path(config["general"]["gd-location"])/key ]
    else:
        tasks = metaprocessor.helpers.workflow.generate_tasks(config)

    for task in tasks:
        if not task.exists():
            print(f"[red]Provided session file [u]{task}[/u] does not exist.[/red]")
            raise SystemExit(1)

    print(f"[green]Calculating steps for {len(tasks)} session(s).[/green]")

    with ThreadPoolExecutor() as executor:
        executor.map(
            metaprocessor.helpers.workflow.steps,
            tasks,
            [config]*len(tasks),
        )


@run.command()
@click.option(
    "--key",
    required=False,
    help="Key of the session to be processed.",
)
def report(key: str) -> None:
    """
    Report generation.
    """
    config = metaprocessor.helpers.config.read()

    if key:
        tasks = [ pathlib.Path(config["general"]["gd-location"])/key ]
    else:
        tasks = metaprocessor.helpers.workflow.generate_tasks(config)

    for task in tasks:
        if not task.exists():
            print(f"[red]Provided session file [u]{task}[/u] does not exist.[/red]")
            raise SystemExit(1)

    metaprocessor.helpers.workflow.report(tasks)
