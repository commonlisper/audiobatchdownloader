import validators

from colors import Color
from answer import Answer
import extensions

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


def get_input(msg: str) -> str:
    return input(msg).lower()


def request_user_data() -> list[tuple[str, str, str]]:
    print(C.text_magenta(".:: Please, input some data. ::.\n"))

    inputs: list[tuple[str, str, str]] = []
    while True:
        url = process_url()
        file_extension = process_extension()
        path_to_save = get_input("Enter the absolute path on your computer to store files: ")

        input_info = (url, file_extension, path_to_save)
        inputs.append(input_info)

        if get_input(f"Do you want to add more? ({Answer.YES.value}/{Answer.NO.value}): ").startswith(Answer.NO.value):
            break

    return inputs


def process_url() -> str:
    while True:
        url = get_input(C.text_cyan("Enter the URL from which you wish to download files: "))
        is_valid = validate_url(url)

        if is_valid:
            return url

        print(C.text_red("The URL you entered is not valid, please enter it again"))
        C.reset_style()


def validate_url(url: str) -> bool:
    validation_result = validators.url(url)

    if isinstance(validation_result, validators.ValidationError):
        return False

    return validation_result


def process_extension() -> str:
    while True:
        extension = get_input(C.text_cyan("Select the type of file you wish to download (mp3, pdf, midi): "))
        is_valid_extension = validate_extension(extension)

        if is_valid_extension:
            return extension

        print(C.text_red("The file extension you entered is not valid, please enter it again"))
        C.reset_style()


def validate_extension(ext: str) -> bool:
    if ext in extensions.ALL:
        return True

    return False


def show_process_message(url: str) -> None:
    print(f"\nProcessing => {url}")


def show_finish_message() -> None:
    print(C.text_magenta("Finished processing.\n"))
