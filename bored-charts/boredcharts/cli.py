import argparse
import asyncio
from pathlib import Path

from boredcharts.pdf import UrlToPdfFile, print_to_pdf_manual


def init() -> None:
    """create a new project scaffolding"""
    raise NotImplementedError


def list_() -> None:
    """list available reports"""
    raise NotImplementedError


def export(report: str, *, writer: UrlToPdfFile = print_to_pdf_manual) -> None:
    """write to pdf

    TODO:
    - [x] write to pdf
    - [ ] spin up server
    - [ ] provide list of reports
    """
    url = f"http://localhost:4000/{report}"  # TODO: spin up server & replace base url
    file = Path(report).absolute().with_suffix(".pdf")
    asyncio.run(writer(url, file))
    print(f"Exported {report} to {file}")


def dev() -> None:
    """run uvicorn with reload"""
    raise NotImplementedError


def serve() -> None:
    """run uvicorn without reload"""
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="boredcharts CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    parser_init = subparsers.add_parser("init", help="Create a new project scaffolding")
    parser_init.set_defaults(func=init)

    parser_init = subparsers.add_parser("list", help="List available reports")
    parser_init.set_defaults(func=list_)

    parser_export = subparsers.add_parser("export", help="Write to PDF")
    parser_export.add_argument("report", type=str, help="The report to export")
    parser_export.set_defaults(func=export)

    parser_dev = subparsers.add_parser("dev", help="Run uvicorn with reload")
    parser_dev.set_defaults(func=dev)

    parser_serve = subparsers.add_parser("serve", help="Run uvicorn without reload")
    parser_serve.set_defaults(func=serve)

    args = parser.parse_args()

    func_args = {k: v for k, v in vars(args).items() if k != "func" and k != "command"}
    args.func(**func_args)
