import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import bs4
import requests

from colors import Color

c = Color()


def request_user_data() -> list[tuple[str, str, str]]:
    """
    Request user data such as
    url,
    file extension,
    path to save
    from input stream and return tuple with these values.
    """
    print(
        c.text_green(
            """.:: Hello ans welcome to AudioBatchDownloader!
You can download multiple files on the one web page with it!
Also you can input many urls. ::.
"""
        )
    )
    print(c.text_magenta(".:: Please, input some data. ::."))

    inputs: list[tuple[str, str, str]] = []
    while True:
        # TODO: add user input validation in future.

        url = input(c.text_cyan("Enter url from witch you want to download files: "))

        file_extension = input(
            "Enter what type of file you want to download from(mp3, pdf, midi): "
        )

        path_to_save = input("Enter absolute path on your computer to save files: ")
        path_to_save = check_file_path(path_to_save)

        input_info = (url, file_extension, path_to_save)
        inputs.append(input_info)

        if input("Do you want to add more? (y/n): ").lower()[0] == "n":
            break

    return inputs


def check_file_path(path_to_save) -> str:
    """
    Checks if the path exists and creates it if not.
    Return absolute path where to save the file
    """
    path = Path(path_to_save)
    if not path.exists():
        path.mkdir()

    path_to_save = str(path.absolute())
    return path_to_save


def get_domain_from_url(url: str) -> str:
    """
    Return domain which consist from scheme and domain name.
    """
    url_parsed = urlparse(url)
    return f"{url_parsed.scheme}://{url_parsed.netloc}/"


def get_html(url: str) -> str:
    """
    Return html code from specified url.
    """
    response = requests.get(url)
    html = response.text

    return html


def get_file_urls(html: str, extension: str) -> list[str]:
    """
    Return list of files href from html code with specified extension.
    """
    soup = bs4.BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    hrefs = [tag["href"] for tag in a_tags if tag["href"].endswith(extension)]

    return hrefs


def get_full_file_url(domain: str, href: str, path: str) -> tuple[str, str]:
    """
    Return formed full file url.
    """
    filename = href.split("/")[-1]
    full_file_url = f"{domain}{href[1:]}" if href.startswith("/") else f"{domain}{href}"
    full_file_path = f"{path}{os.sep}{filename}"

    return full_file_url, full_file_path


def download_file(file_info: tuple[str, str]) -> None:
    """
    Download one file from url in first param
    and save it to file path in second param.
    """
    url, save_file_path = file_info
    response = requests.get(url)
    with open(save_file_path, mode="wb") as file:
        file.write(response.content)

    print(f"file at url = {url} saved to {save_file_path}")


def download_files(files_url: list[str], domain: str, path: str) -> None:
    """
    Download all files to the disk with ThreadPoolExecutor.
    """
    files = [get_full_file_url(domain, href, path) for href in files_url]

    with ThreadPoolExecutor() as executor:
        executor.map(download_file, files)


def main() -> None:
    inputs = request_user_data()
    c.reset_style()
    for url, file_extension, path_to_save in inputs:
        print(f"\nProcessing => {url}")
        html = get_html(url)
        file_urls = get_file_urls(html, file_extension)
        domain = get_domain_from_url(url)
        download_files(file_urls, domain, path_to_save)
        print("Finished processing.\n")


if __name__ == "__main__":
    main()
