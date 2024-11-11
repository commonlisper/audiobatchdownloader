import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import bs4
import requests

import console_ui as cui


def get_domain_from_url(url: str) -> str:
    url_parsed = urlparse(url)
    return f"{url_parsed.scheme}://{url_parsed.netloc}/"


def get_html(url: str) -> str:
    try:
        response = requests.get(url)
        html = response.text

        return html
    except requests.RequestException as e:
        cui.show_error_while_fetching_html(url, e)
        return ""


def get_files_path(html: str, extension: str) -> list[str]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    paths = [a["href"] for a in a_tags if a["href"].endswith(extension)]

    return paths


def make_file_url_and_path(domain: str, path: str, path_to_save: str) -> tuple[str, str]:
    filename = path.split("/")[-1]
    full_file_url = f"{domain}{path[1:]}" if path.startswith("/") else f"{domain}{path}"
    full_file_path = f"{path_to_save}{os.sep}{filename}"

    return full_file_url, full_file_path


def download_file(file_info: tuple[str, str]) -> None:
    file_url, path_to_save = file_info

    try:
        response = requests.get(file_url)

        with open(path_to_save, mode="wb") as file:
            file.write(response.content)

        cui.show_downloaded_file_info(file_url, path_to_save)
    except requests.RequestException as e:
        cui.show_error_while_file_download(file_url, e)


def download_files(files_path: list[str], domain: str, path_to_save: str) -> None:
    files = [make_file_url_and_path(domain, path, path_to_save) for path in files_path]

    with ThreadPoolExecutor() as executor:
        executor.map(download_file, files)


def process_data(input_data: list[tuple]) -> None:
    for url, file_extension, path_to_save in input_data:
        cui.show_process_message(url)

        html = get_html(url)
        if not html:
            continue

        file_urls = get_files_path(html, file_extension)
        if not file_urls:
            cui.show_no_file_message(file_extension)
            continue

        domain = get_domain_from_url(url)
        download_files(file_urls, domain, path_to_save)

        cui.show_finish_message()


def main() -> None:
    cui.show_welcome_message()
    inputs = cui.request_user_data()
    process_data(inputs)


if __name__ == "__main__":
    main()
