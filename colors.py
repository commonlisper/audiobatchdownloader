import colorama


class Color:
    def __init__(self) -> None:
        """Colorama init."""
        self.c = colorama
        self.c.init()

    def text_green(self, text: str) -> str:
        """Return text with `green` color using colorama lib."""
        return self.c.Fore.GREEN + text

    def text_magenta(self, text: str) -> str:
        """Return text with `magenta` color using colorama lib."""
        return self.c.Fore.MAGENTA + text

    def text_cyan(self, text: str) -> str:
        """Return text with `cyan` color using colorama lib."""
        return self.c.Fore.CYAN + text

    def reset_style(self):
        """Reset console colors."""
        print(self.c.Style.RESET_ALL)

    def __del__(self):
        self.reset_style()
