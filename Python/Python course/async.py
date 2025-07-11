import asyncio
from pathlib import Path
from time import perf_counter

import aiohttp
import requests

ROOT_DIR = Path(__file__).parent
DOWNLOAD_DIR = ROOT_DIR / "downloads"
IMG_URL_TEMPLATE = "https://httpcats.com/{}.jpg"

DOWNLOAD_DIR.mkdir(exist_ok=True)


def download_content(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, "wb") as fout:
        fout.write(response.content)


async def download_content_async(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            with open(file_path, "wb") as fout:
                fout.write(await resp.read())


async def main():
    codes = list(range(400, 450))
    print("STARTING TO DOWNLOAD")
    print(f"{len(codes)} codes in queue.")
    print("-" * 30)

    start = perf_counter()
    tasks = []

    for i in codes:
        url = IMG_URL_TEMPLATE.format(i)
        file_path = DOWNLOAD_DIR / f"cat_status_code{i}.jpg"
        tasks.append(
            asyncio.create_task(download_content_async(url, file_path)))

    await asyncio.gather(*tasks, return_exceptions=True) # '*' upackages the list of tasks into seperable coroutines (tasks)

    print(f"FINISH in {perf_counter() - start}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
