import colorama


def init() -> None:
    """Colorama init."""
    colorama.init()


def text_green(text: str) -> str:
    """Return text with `green` color using colorama lib."""
    return colorama.Fore.GREEN + text


def text_magenta(text: str) -> str:
    """Return text with `magenta` color using colorama lib."""
    return colorama.Fore.MAGENTA + text


def text_cyan(text: str) -> str:
    """Return text with `cyan` color using colorama lib."""
    return colorama.Fore.CYAN + text


def reset_style():
    """Reset console colors."""
    print(colorama.Style.RESET_ALL)
