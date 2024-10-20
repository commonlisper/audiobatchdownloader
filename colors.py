import colorama


class Color:
    def __init__(self) -> None:
        self.c = colorama
        self.c.init()

    def text_green(self, text: str) -> str:
        return self.c.Fore.GREEN + text

    def text_magenta(self, text: str) -> str:
        return self.c.Fore.MAGENTA + text

    def text_cyan(self, text: str) -> str:
        return self.c.Fore.CYAN + text

    def text_red(self, text: str) -> str:
        return self.c.Fore.RED + text

    def reset_style(self):
        print(self.c.Style.RESET_ALL)

    def __del__(self):
        self.reset_style()
