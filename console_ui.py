from collections.abc import Callable
from pathlib import Path

import validators

import extensions
from answer import Answer
from colors import Color

# for text coloring via console
_C = Color()


def show_welcome_message() -> None:
    _C.reset_style()

    print(
        _C.text_green(
            """.:: Hello ans welcome to AudioBatchDownloader!
    You can download multiple files on the one web page with it!
    Also you can input many urls. ::.
    """
        )
    )


def request_user_data() -> list[tuple[str, str, str]]:
    print(_C.text_magenta(".:: Please, input some data. ::.\n"))

    inputs: list[tuple[str, str, str]] = []
    while True:
        url = process_url()
        file_extension = process_extension()
        path_to_save = resolve_path(process_path())

        input_info = (url, file_extension, str(path_to_save))
        inputs.append(input_info)

        if get_input(f"Do you want to add more? ({Answer.YES.value}/{Answer.NO.value}): ").startswith(Answer.NO.value):
            break

    return inputs


def process_input(input_msg: str, validator: Callable, error_msg: str) -> str:
    while True:
        inpt = get_input(_C.text_cyan(input_msg))
        is_valid_inpt = validator(inpt)

        if is_valid_inpt:
            return inpt

        show_error(error=error_msg)


def get_input(msg: str) -> str:
    return input(msg).lower()


def show_error(error: str) -> None:
    print(_C.text_red(error))
    _C.reset_style()


def process_url() -> str:
    url = process_input(
        input_msg="Enter the URL from which you wish to download files: ",
        validator=validate_url,
        error_msg="The URL you entered is not valid, please enter it again",
    )

    return url


def validate_url(url: str) -> bool:
    validation_result = validators.url(url)

    if isinstance(validation_result, validators.ValidationError):
        return False

    return validation_result


def process_extension() -> str:
    extension = process_input(
        input_msg="Select the type of file you wish to download (mp3, pdf, midi): ",
        validator=validate_extension,
        error_msg="The file extension you entered is not valid, please enter it again",
    )

    return extension


def validate_extension(ext: str) -> bool:
    if ext in extensions.ALL:
        return True

    return False


def process_path() -> str:
    path = process_input(
        input_msg="Enter your computer's file storage path: ",
        validator=validate_path,
        error_msg="The path you entered is not valid, please enter it again",
    )

    return path


# func with `smell`
def validate_path(path: str) -> bool:
    # create path and make absolute
    p = resolve_path(path)

    # after creation, check that it has been created
    if not p.is_dir():
        return False

    return True


def resolve_path(path: str) -> Path:
    p = Path(path)

    if not p.exists():
        p.mkdir()

    return p.absolute()


def show_process_message(url: str) -> None:
    print(f"\nProcessing => {url}")


def show_finish_message() -> None:
    print(_C.text_magenta("Finished processing.\n"))


def show_no_file_message(extension: str) -> None:
    print(_C.text_red(f"No files found with the extension .{extension}"))
