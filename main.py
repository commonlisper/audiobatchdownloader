from urllib.parse import urlparse
import urllib.request as req
from pathlib import Path
import bs4
import os


# URL = "https://www.john-scrivo.de/lessons.htm"
# FILE_EXTENSION = "pdf"
# PATH_TO_SAVE = "C:\Users\active\Downloads"


def request_user_data() -> tuple:
    print("Hello ans welcome to AudioBatchDownloader!")
    print("Please, input some data.")

    url = input("Enter url from witch you want to download files: ")

    file_extension = input(
        "Enter what type of file you want to download from(mp3, pdf, midi): "
    )

    path_to_save = input("Enter absolute path on your computer to save files: ")
    path = Path(path_to_save)
    if not path.exists():
        path.mkdir()
    path_to_save = str(path.absolute())

    return url, file_extension, path_to_save


def get_domain_from_url(url: str) -> str:
    url_parsed = urlparse(url)
    return f"{url_parsed.scheme}://{url_parsed.netloc}/"


def get_html(url: str) -> str:
    with req.urlopen(url) as res:
        html = res.read()

    return html


def get_file_urls_from(html: str, extension: str) -> list[str]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    hrefs = [tag["href"] for tag in a_tags if tag["href"].endswith(extension)]

    return hrefs


def download_and_save_files(files_url: list[str], domain: str, path: str) -> None:
    for href in files_url:
        full_file_path, full_file_url = get_full_file_url(domain, href, path)
        req.urlretrieve(full_file_url, full_file_path)
        print(f"file at url = {full_file_url} saved to {full_file_path}")


def get_full_file_url(domain, href, path):
    filename = href.split("/")[-1]
    full_file_url = f"{domain}{href[1:]}" if href.startswith("/") else f"{domain}{href}"
    full_file_path = f"{path}{os.sep}{filename}"
    return full_file_path, full_file_url


def main() -> None:
    url, file_extension, path_to_save = request_user_data()
    html = get_html(url)
    file_urls = get_file_urls_from(html, file_extension)
    domain = get_domain_from_url(url)
    download_and_save_files(file_urls, domain, path_to_save)


if __name__ == "__main__":
    main()
