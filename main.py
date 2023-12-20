import os
import urllib.request as req
from pathlib import Path
from urllib.parse import urlparse

import bs4
import requests
from concurrent.futures import ThreadPoolExecutor


def request_user_data() -> tuple[str, str, str]:
    """
    Request user data such as
    url,
    file extension,
    path to save
    from input stream and return tuple with these values.
    """
    print("Hello ans welcome to AudioBatchDownloader!")
    print("Please, input some data.")

    url = input("Enter url from witch you want to download files: ")

    file_extension = input(
        "Enter what type of file you want to download from(mp3, pdf, midi): "
    )

    path_to_save = input("Enter absolute path on your computer to save files: ")
    path_to_save = check_file_path(path_to_save)

    return url, file_extension, path_to_save


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
    with req.urlopen(url) as res:
        html = res.read()

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


def download_file(file: tuple[str, str]) -> None:
    """
    Download one file from url in first param
    and save it to file path in second param.
    """
    url, save_file_path = file
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
    url, file_extension, path_to_save = request_user_data()
    html = get_html(url)
    file_urls = get_file_urls(html, file_extension)
    domain = get_domain_from_url(url)
    download_files(file_urls, domain, path_to_save)


if __name__ == "__main__":
    main()
