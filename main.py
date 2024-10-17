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
        print(f"Error fetching HTML from {url}: {e}")
        return ""


def get_file_urls(html: str, extension: str) -> list[str]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    hrefs = [tag["href"] for tag in a_tags if tag["href"].endswith(extension)]

    return hrefs


def get_full_file_url(domain: str, href: str, path: str) -> tuple[str, str]:
    filename = href.split("/")[-1]
    full_file_url = f"{domain}{href[1:]}" if href.startswith("/") else f"{domain}{href}"
    full_file_path = f"{path}{os.sep}{filename}"

    return full_file_url, full_file_path


def download_file(file_info: tuple[str, str]) -> None:
    url, save_file_path = file_info
    response = requests.get(url)
    with open(save_file_path, mode="wb") as file:
        file.write(response.content)

    print(f"file at url = {url} saved to {save_file_path}")


def download_files(files_url: list[str], domain: str, path: str) -> None:
    files = [get_full_file_url(domain, href, path) for href in files_url]

    with ThreadPoolExecutor() as executor:
        executor.map(download_file, files)


def main() -> None:
    cui.show_welcome_message()
    inputs = cui.request_user_data()

    for url, file_extension, path_to_save in inputs:
        print(f"\nProcessing => {url}")
        html = get_html(url)
        file_urls = get_file_urls(html, file_extension)
        domain = get_domain_from_url(url)
        download_files(file_urls, domain, path_to_save)
        print("Finished processing.\n")


if __name__ == "__main__":
    main()
