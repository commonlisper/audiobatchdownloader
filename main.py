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

    return (url, file_extension, path_to_save)


def get_domain_from_url(url: str) -> str:
    url_parsed = urlparse(url)
    return f"{url_parsed.scheme}://{url_parsed.netloc}/"


def get_html_from(url: str) -> str:
    with req.urlopen(url) as res:
        html = res.read()

    return html


def get_file_urls_from(html: str, extension: str) -> list[str]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    hrefs = [tag["href"] for tag in a_tags if tag["href"].endswith(extension)]

    return hrefs


def save_files_to(files_url: list[str], domain: str, path: str) -> None:
    for href in files_url:
        filename = href.split("/")[-1]
        file_url = f"{domain}{href[1:]}" if href.startswith("/") else f"{domain}{href}"
        full_file_path = f"{path}{os.sep}{filename}"
        print(file_url)
        print(full_file_path)
        req.urlretrieve(file_url, full_file_path)
        print(f"file at url = {file_url} saved to {full_file_path}")


def main() -> None:
    url, file_extension, path_to_save = request_user_data()
    html = get_html_from(url)
    file_urls = get_file_urls_from(html, file_extension)
    domain = get_domain_from_url(url)
    save_files_to(file_urls, domain, path_to_save)


if __name__ == "__main__":
    main()
