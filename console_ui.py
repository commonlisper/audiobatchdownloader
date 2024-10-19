from colors import Color
from answer import Answer

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
    C.reset_style()

    print(C.text_magenta(".:: Please, input some data. ::."))

    inputs: list[tuple[str, str, str]] = []
    while True:
        # TODO: add user input validation in future.

        url = input(C.text_cyan("Enter the URL from which you wish to download files: "))
        file_extension = input("Select the type of file you wish to download (mp3, pdf, midi): ")
        path_to_save = input("Enter the absolute path on your computer to store files: ")

        input_info = (url, file_extension, path_to_save)
        inputs.append(input_info)

        if (
            input(f"Do you want to add more? ({Answer.YES.value}/{Answer.NO.value}): ")
            .lower()
            .startswith(Answer.NO.value)
        ):
            break

    return inputs


def show_process_message(url: str) -> None:
    print(f"\nProcessing => {url}")


def show_finish_message() -> None:
    print("Finished processing.\n")
