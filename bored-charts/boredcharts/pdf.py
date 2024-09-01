import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Protocol

from playwright.async_api import async_playwright


class UrlToPdfFile(Protocol):
    async def __call__(self, url: str, file: Path) -> None: ...


async def print_to_pdf_manual(url: str, file: Path) -> None:
    """this one seems to work the best"""
    async with async_playwright() as p:
        args = [
            "--headless=new",
            "--virtual-time-budget=10000",  # seems to wait for ajax too?
            "--run-all-compositor-stages-before-draw",  # also recommended, dunno
            "--no-pdf-header-footer",
            f"--print-to-pdf={file.as_posix()}",
            url,
        ]
        process = await asyncio.create_subprocess_exec(
            p.chromium.executable_path,
            *args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, stderr = await process.communicate()

        if process.returncode != 0:
            raise ChildProcessError(f"Could not export to pdf {stderr.decode()}")


async def _print_to_pdf_pw_adv(url: str, file: Path) -> None:
    # in headless mode this doesn't seem to actually download the pdf
    prefs = {
        "printing": {
            "print_preview_sticky_settings": {
                "appState": json.dumps(
                    {
                        "version": 2,
                        "recentDestinations": [
                            {"id": "Save as PDF", "origin": "local", "account": ""}
                        ],
                        "selectedDestinationId": "Save as PDF",
                        "isHeaderFooterEnabled": False,
                    }
                )
            }
        },
    }
    with tempfile.TemporaryDirectory() as pref_dir:
        pref_file = Path(pref_dir) / "Default" / "Preferences"
        pref_file.parent.mkdir(parents=True, exist_ok=True)
        with pref_file.open("w") as f:
            json.dump(prefs, f)

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=pref_file.parent.parent,
                ignore_default_args=["--headless"],
                args=[
                    "--headless=new",
                    "--kiosk-printing",
                ],
            )
            page = await context.new_page()

            await page.goto(url, wait_until="networkidle")
            await page.evaluate("window.print();")
            await context.close()


async def _print_to_pdf_pw_basic(url: str, file: Path) -> None:
    # playwright's built-in pdf export results in text that can't be selected well
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle")
        await page.pdf(
            path=file,
            format="A4",
            margin={"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"},
        )
        await context.close()
        await browser.close()
