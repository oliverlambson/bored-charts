import argparse
import asyncio
import importlib
import multiprocessing
import time
from pathlib import Path
from typing import Literal, NamedTuple
from urllib.error import URLError
from urllib.request import urlopen

import uvicorn
from fastapi import FastAPI
from starlette.routing import NoMatchFound

from boredcharts.cli.discover import get_import_string
from boredcharts.pdf import UrlToPdfFile, print_to_pdf_manual


class Report(NamedTuple):
    name: str
    urlpath: str
    tag: str


def get_report_url(
    path: Path | None,
    app_name: str | None,
    name: str,
) -> str:
    import_str = get_import_string(path=path, app_name=app_name)  # mutates sys.path
    mod = importlib.import_module(import_str.split(":")[0])
    app = getattr(mod, import_str.split(":")[1])
    assert isinstance(app, FastAPI)
    return app.url_path_for(name)


def get_reports(
    path: Path | None,
    app_name: str | None,
) -> list[Report]:
    import_str = get_import_string(path=path, app_name=app_name)  # mutates sys.path
    mod = importlib.import_module(import_str.split(":")[0])
    app = getattr(mod, import_str.split(":")[1])
    assert isinstance(app, FastAPI)
    openapi = app.openapi()
    paths = openapi["paths"]
    assert isinstance(paths, dict)

    reports: list[Report] = []
    for urlpath, methods in paths.items():
        assert isinstance(urlpath, str)
        assert isinstance(methods, dict)
        for method, data in methods.items():
            assert isinstance(method, str)
            assert isinstance(data, dict)
            if method != "get":
                continue

            tags = data.get("tags")
            if tags is None:
                continue
            assert isinstance(tags, list)
            tags = [t for t in tags if t.startswith("report")]  # boredcharts convention
            if not tags:
                continue

            name = data.get("summary")
            assert isinstance(name, str)
            name = name.lower().replace(" ", "_")  # reverse fastapi name->summary
            if name.startswith("index"):  # boredcharts convention
                continue

            for tag in tags:
                reports.append(Report(name=name, urlpath=urlpath, tag=tag))

    return reports


def _run_uvicorn(
    path: Path | None,
    app_name: str | None,
    reload: bool = False,
    host: str = "127.0.0.1",
    port: int = 4000,
    log_level: Literal[
        "critical",
        "error",
        "warning",
        "info",
        "debug",
        "trace",
    ] = "info",
) -> None:
    import_str = get_import_string(path=path, app_name=app_name)
    uvicorn.run(
        import_str,
        host=host,
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=reload,
        log_level=log_level,
    )


def init(
    path: Path | None,
    app_name: str | None,
) -> None:
    """create a new project scaffolding"""
    raise NotImplementedError


def list_reports(
    path: Path | None,
    app_name: str | None,
) -> None:
    """list available reports"""
    reports = get_reports(path, app_name)
    reports = sorted(reports, key=lambda x: f"{x.tag}::{x.name}")
    urlpathwidth = max(len(r.urlpath) for r in reports)
    name = max(len(r.name) for r in reports)
    tagwidth = max(len(r.tag) for r in reports)
    print(
        f"{"REPORT".ljust(name)}  {"CATEGORY".ljust(tagwidth)}  {"URL".ljust(urlpathwidth)}"
    )
    for r in reports:
        category = ":".join(r.tag.split(":")[1:]) or "-"  # boredcharts convention
        print(
            f"{r.name.ljust(name)}  {category.ljust(tagwidth)}  {r.urlpath.ljust(urlpathwidth)}"
        )


def export(
    path: Path | None,
    app_name: str | None,
    report: str,
    *,
    exporter: UrlToPdfFile = print_to_pdf_manual,
) -> None:
    """write to pdf

    TODO:
    - [x] write to pdf
    - [x] spin up server
    - [x] provide list of reports
    """
    try:
        route = get_report_url(path, app_name, report)
    except NoMatchFound:
        print(f'Report "{report}" not found!')
        print("Use `boredcharts list` to see available reports.")
        raise SystemExit(1)

    host = "127.0.0.1"
    port = 4001  # different port just for exports
    base_url = f"http://{host}:{port}"
    process = multiprocessing.Process(
        target=_run_uvicorn,
        kwargs=dict(
            path=path,
            app_name=app_name,
            reload=False,
            host=host,
            port=port,
            log_level="warning",
        ),
    )

    print("Spinning up boredcharts app", end="", flush=True)
    process.start()
    for _ in range(10):
        print(".", end="", flush=True)
        time.sleep(0.1)
        try:
            with urlopen(f"{base_url}/healthz") as response:
                status = response.status
        except URLError:
            continue
        if status == 200:
            print(" started!")
            break
    else:
        print(" health check failed!")
        raise Exception("Couldn't start app!")

    url = f"{base_url}{route}"
    file = Path(report.replace(".", "-")).absolute().with_suffix(".pdf")
    asyncio.run(exporter(url, file))
    print(f"Exported {report} to {file}")

    process.terminate()


def dev(path: Path | None, app_name: str | None) -> None:
    """run uvicorn with reload"""
    _run_uvicorn(path, app_name, reload=True)


def run(path: Path | None, app_name: str | None) -> None:
    """run uvicorn without reload"""
    _run_uvicorn(path, app_name, reload=False)


def main() -> None:
    """cli entrypoint"""
    parser = argparse.ArgumentParser(description="boredcharts CLI")
    parser.add_argument("path", type=Path, default=None, help="Path to FastAPI app")
    parser.add_argument("--app-name", type=str, default=None, help="FastAPI app name")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    parser_init = subparsers.add_parser("init", help="Create a new project scaffolding")
    parser_init.set_defaults(func=init)

    parser_init = subparsers.add_parser("list", help="List available reports")
    parser_init.set_defaults(func=list_reports)

    parser_export = subparsers.add_parser("export", help="Write report to PDF")
    parser_export.add_argument("report", type=str, help="The report to export")
    parser_export.set_defaults(func=export)

    parser_dev = subparsers.add_parser("dev", help="Run uvicorn with reload")
    parser_dev.set_defaults(func=dev)

    parser_serve = subparsers.add_parser("run", help="Run uvicorn without reload")
    parser_serve.set_defaults(func=run)

    args = parser.parse_args()

    func_args = {k: v for k, v in vars(args).items() if k != "func" and k != "command"}
    args.func(**func_args)
