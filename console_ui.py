from pathlib import Path
from colors import Color

C = Color()


def show_welcome_message() -> None:
    C.reset_style()

    print(
        C.text_green(
            """.:: Hello ans welcome to AudioBatchDownloader!
    You can download multiple files on the one web page with it!
    Also you can input many urls. ::.
    """
        )
    )


def request_user_data() -> list[tuple[str, str, str]]:

    print(C.text_magenta(".:: Please, input some data. ::."))

    inputs: list[tuple[str, str, str]] = []
    while True:
        # TODO: add user input validation in future.

        url = input(C.text_cyan("Enter the URL from which you wish to download files: "))
        file_extension = input("Select the type of file you wish to download (mp3, pdf, midi): ")
        path_to_save = input("Enter the absolute path on your computer to store files: ")

        path_to_save = _check_file_path(path_to_save)

        input_info = (url, file_extension, path_to_save)
        inputs.append(input_info)

        if input("Do you want to add more? (y/n): ").lower().startswith("n"):
            break

    return inputs


def _check_file_path(path_to_save: str) -> str:
    path = Path(path_to_save)
    if not path.exists():
        path.mkdir()

    path_to_save = str(path.absolute())
    return path_to_save


def show_process_message(url: str) -> None:
    print(f"\nProcessing => {url}")


def show_finish_message() -> None:
    print("Finished processing.\n")
