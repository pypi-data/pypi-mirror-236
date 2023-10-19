#!/usr/bin/env python3
from __future__ import annotations

import json as json_mod
import logging
import os
import subprocess
import sys
from functools import lru_cache
from typing import Any, Dict, List, Optional

import click
from tabulate import tabulate
from toolforge_weld.config import Config
from toolforge_weld.errors import ToolforgeError, print_error_context, ToolforgeUserError

from toolforge_builds_cli.build import BuildClient
from toolforge_builds_cli.config import get_loaded_config

LOGGER = logging.getLogger("toolforge" if __name__ == "__main__" else __name__)

STATUS_STYLE = {
    "unknown": click.style("unknown", fg="yellow"),
    "running": click.style("running", fg="yellow"),
    "ok": click.style("ok", fg="green"),
    "cancelled": click.style("cancelled", fg="green"),
    "error": click.style("error", fg="red"),
    "timeout": click.style("timeout", fg="red"),
}


def _ctx_is_debug() -> bool:
    return click.get_current_context().obj["debug"]


def handle_error(e: Exception, debug: bool = False) -> None:
    user_error = isinstance(e, ToolforgeUserError)

    prefix = "Error: "
    if not user_error:
        prefix = f"{e.__class__.__name__}: "

    click.echo(click.style(f"{prefix}{e}", fg="red"))

    if debug:
        LOGGER.exception(e)

        if isinstance(e, ToolforgeError):
            print_error_context(e)
    elif not user_error:
        click.echo(
            click.style(
                "Please report this issue to the Toolforge admins if it persists: https://w.wiki/6Zuu",
                fg="red",
            )
        )


@lru_cache(maxsize=None)
def _load_config_from_ctx() -> Config:
    ctx = click.get_current_context()
    return ctx.obj["config"]


def _format_run(run: Dict[str, Any]) -> Dict[str, Any]:
    start_time = run["start_time"] if run["start_time"] else "N/A"
    end_time = run["end_time"] if run["end_time"] else "N/A"
    ref = run["parameters"]["ref"] if run["parameters"]["ref"] else "N/A"
    status = run["status"].split("_")[1].lower()
    if status == "success":
        status = "ok"
    elif status == "failure":
        status = "error"

    return {
        "build_id": run["build_id"],
        "start_time": start_time,
        "end_time": end_time,
        "status": status,
        "message": run["message"],
        "ref": ref,
        "source_url": run["parameters"]["source_url"],
        "destination_image": run["destination_image"],
    }


def _runs_to_table(runs: List[Dict[str, Any]]) -> List[Any]:
    headers = [
        "build_id",
        "status",
        "start_time",
        "end_time",
        "source_url",
        "ref",
        "destination_image",
    ]
    headers = [click.style(header, bold=True) for header in headers]
    runs_values = []
    for run in runs:
        run_values = [
            run["build_id"],
            STATUS_STYLE[run["status"]],
            run["start_time"],
            run["end_time"],
            run["source_url"],
            run["ref"],
            run["destination_image"],
        ]
        runs_values.append(run_values)
    return [headers, runs_values]


def _get_formatted_run_str(run: Dict[str, Any]) -> str:
    run_str = ""
    run_str += f"{click.style('Build ID:', bold=True)} {click.style(run['build_id'], fg='blue')}\n"
    run_str += f"{click.style('Start Time:', bold=True)} {run['start_time']}\n"
    run_str += f"{click.style('End Time:', bold=True)} {run['end_time']}\n"
    run_str += f"{click.style('Status:', bold=True)} {STATUS_STYLE[run['status']]}\n"
    run_str += f"{click.style('Message:', bold=True)} {run['message']}\n"
    run_str += click.style("Parameters:\n", bold=True)
    run_str += f"    {click.style('Source URL:', bold=True)} {run['source_url']}\n"
    run_str += f"    {click.style('Ref:', bold=True)} {run['ref']}\n"
    run_str += f"{click.style('Destination Image:', bold=True)} {run['destination_image']}"

    return run_str


@click.version_option(prog_name="Toolforge Builds CLI")
@click.group(name="build", help="Toolforge build command line")
@click.option(
    "-v",
    "--verbose",
    help="Show extra verbose output. NOTE: Do no rely on the format of the verbose output",
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_VERBOSE", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.option(
    "-d",
    "--debug",
    help="show logs to debug the toolforge-build-* packages. For extra verbose output, see --verbose",
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_DEBUG", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.pass_context
def toolforge_build(ctx: click.Context, verbose: bool, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["config"] = get_loaded_config()
    pass


@toolforge_build.command(name="start", help="Start a pipeline to build a container image from source code")
@click.argument("SOURCE_GIT_URL", required=False)
@click.option(
    "--ref",
    help="Branch, tag or commit to build, by default will use the HEAD of the given repository.",
    show_default=True,
)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
def build_start(
    source_git_url: str,
    ref: Optional[str] = None,
    json: bool = False,
) -> None:
    if not source_git_url:
        message = (
            f"{click.style('Error:', bold=True, fg='red')} Please provide a git url for your source code.\n"
            + f"{click.style('Example:', bold=True)}"
            + " toolforge build start 'https://gitlab.wikimedia.org/toolforge-repos/my-tool'"
        )
        click.echo(message)
        sys.exit(1)

    config = _load_config_from_ctx()
    build_client = BuildClient.from_config(config=config)
    data = {"source_url": source_git_url}
    if ref:
        data["ref"] = ref

    new_build = build_client.post("/build", json=data)

    if json:
        click.echo(json_mod.dumps(new_build, indent=4))
    else:
        click.echo(
            f"Building '{new_build['parameters']['source_url']}', build name is '{new_build['name']}'\n"
            f"You can see the status with:\n\ttoolforge build show"
        )


@toolforge_build.command(name="logs", help="Show the logs for a build")
@click.argument("RUN_NAME", required=False)
def build_logs(run_name: Optional[str]) -> None:
    config = _load_config_from_ctx()
    builds_client = BuildClient.from_config(config=config)
    if not run_name:
        last_build = builds_client.get("/build/latest")
        run_name = last_build["build_id"]

    logs = builds_client.get(f"/build/{run_name}/logs")
    for log in logs["lines"]:
        click.echo(log)


@toolforge_build.command(name="list", help="List builds")
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
def build_list(json: bool) -> None:
    config = _load_config_from_ctx()
    builds_client = BuildClient.from_config(config=config)
    runs = builds_client.get("/build")
    if len(runs) == 0:
        click.echo(
            click.style(
                (
                    "No builds found, you can start one using `toolforge build start`,"
                    + "run `toolforge build start --help` for more details"
                ),
                fg="yellow",
            )
        )
        return

    runs = [_format_run(run=run) for run in runs]
    if json:
        for run in runs:
            click.echo(json_mod.dumps(run, indent=4))
        return

    headers, data = _runs_to_table(runs=runs)
    click.echo(
        tabulate(
            data,
            headers=headers,
            tablefmt="plain",
        )
    )


@toolforge_build.command(name="cancel", help="Cancel a running build (does nothing for stopped ones)")
@click.option(
    "--all",
    help="Cancel all the current builds.",
    is_flag=True,
)
@click.option(
    "--yes-i-know",
    "-y",
    help="Don't ask for confirmation.",
    is_flag=True,
)
@click.argument(
    "build_ids",
    nargs=-1,
)
def build_cancel(build_ids: List[str], all: bool, yes_i_know: bool) -> None:
    if not build_ids and not all:
        message = (
            f"{click.style('Error:', bold=True, fg='red')} No run passed to cancel.\n"
            + f"{click.style('Example:', bold=True)}"
            + " toolforge build cancel <build-id>"
        )
        click.echo(message)
        sys.exit(1)

    config = _load_config_from_ctx()
    builds_client = BuildClient.from_config(config=config)

    if not yes_i_know:
        click.confirm(f"I'm going to cancel {len(build_ids)} runs, continue?", abort=True)

    build_ids_count = len(build_ids)
    for build_id in build_ids:
        try:
            result = builds_client.put(f"/build/{build_id}/cancel")
            if not result:
                build_ids_count -= 1
        except Exception as e:
            handle_error(e, debug=_ctx_is_debug())
            build_ids_count -= 1

    click.echo(f"Cancelled {build_ids_count} runs")


@toolforge_build.command(name="delete", help="Delete a build")
@click.option(
    "--all",
    help="Delete all the current builds",
    is_flag=True,
)
@click.option(
    "--yes-i-know",
    "-y",
    help="Don't ask for confirmation",
    is_flag=True,
)
@click.argument(
    "build_ids",
    nargs=-1,
)
def build_delete(build_ids: List[str], all: bool, yes_i_know: bool) -> None:
    if not build_ids and not all:
        message = (
            f"{click.style('Error:', bold=True, fg='red')} No run passed to delete.\n"
            + f"{click.style('Example:', bold=True)}"
            + " toolforge build delete <build-id>"
        )
        click.echo(message)
        sys.exit(1)

    config = _load_config_from_ctx()
    builds_client = BuildClient.from_config(config=config)

    if not yes_i_know:
        click.confirm(f"I'm going to delete {len(build_ids)} runs, continue?", abort=True)

    build_ids_count = len(build_ids)
    for build_id in build_ids:
        try:
            result = builds_client.delete(f"/build/{build_id}")
            if not result:
                build_ids_count -= 1
        except Exception as e:
            handle_error(e, debug=_ctx_is_debug())
            build_ids_count -= 1

    click.echo(f"Deleted {build_ids_count} runs")


@toolforge_build.command(name="show", help="Show details for a specific build")
@click.argument("RUN_NAME", required=False)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
def build_show(run_name: str, json: bool) -> None:
    config = _load_config_from_ctx()
    builds_client = BuildClient.from_config(config=config)

    if run_name:
        run = builds_client.get(f"/build/{run_name}")
    else:
        run = builds_client.get("/build/latest")

    run = _format_run(run=run)
    if json:
        click.echo(
            json_mod.dumps(
                run,
                indent=4,
            )
        )
    else:
        click.echo(_get_formatted_run_str(run=run))


@toolforge_build.command(name="_commands", hidden=True)
def internal_commands():
    """Used internally for tab completion."""
    for name, command in sorted(toolforge_build.commands.items()):
        if command.hidden:
            continue
        click.echo(name)


def main() -> int:
    res = toolforge_build.parse_args(ctx=click.Context(command=toolforge_build), args=sys.argv)
    debug = "-d" in res or "--debug" in res
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        toolforge_build()
    except subprocess.CalledProcessError as e:
        handle_error(e, debug=debug)
        return e.returncode
    except Exception as e:
        handle_error(e, debug=debug)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
