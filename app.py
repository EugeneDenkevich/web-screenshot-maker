import asyncio
from pathlib import Path
import os
import platform
import flet as ft
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION
from pyppeteer import launch  # noqa: E402


async def get_screenshot(url: str, counter: int):
    result_folder = Path.home() / ".web_screen_shot"
    if not result_folder.exists():
        os.makedirs(result_folder)
    path = result_folder / f"screen-{counter}.png"
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot(path=str(path), fullPage=True)

# https://www.google.com/
# asyncio.get_event_loop().run_until_complete(get_screenshot("https://stackoverflow.com/questions/78023508/pyton-request-html-is-not-downloading-chromium", 1))

async def main(page: ft.Page):
    page.title = "WebScreenShot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 700
    page.window_height = 500
    page.window_resizable = False

    async def start(e):
        if links_list.value == "":
            return
        links = list(map(lambda l: l.strip(), links_list.value.strip().split("\n")))
        counter = 1
        progress_bar.visible = True
        page.update()
        for link in links:
            try:
                await get_screenshot(link, counter)
                counter += 1
            finally:
                progress_bar.visible = False
                page.update()

    def open_depends_os() -> None:
        path = Path.home() / ".web_screen_shot"
        if not path.exists():
            os.makedirs(path)
        os_name = platform.system()
        if os_name.lower() == "windows":
            os.startfile(path)
        elif os_name.lower() == "darwin":
            os.system(f"open {path}")
        elif os_name.lower() == "linux":
            os.system(f"xdg-open {path}")

    def open_folder(e):
        open_depends_os()

    links_list = ft.TextField(width=600, multiline=True, max_lines=13)
    button_start = ft.ElevatedButton("Получить скрины", width=200, on_click=start)
    button_folder = ft.ElevatedButton("Открыть папку", width=200, on_click=open_folder)
    progress_bar = ft.ProgressBar(
        width=600, color=ft.colors.BLUE_600, bgcolor="#eeeeee", visible=False
    )

    page.add(
        ft.Column(
            controls=[
                links_list,
                progress_bar,
                button_start,
                button_folder,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


ft.app(target=main)
