import re

class Color:
    ANSI_RESET = "\033[0m"

    ANSI_BLACK = "\033[30m"
    ANSI_RED = "\033[31m"
    ANSI_GREEN = "\033[32m"
    ANSI_YELLOW = "\033[33m"
    ANSI_BLUE = "\033[34m"
    ANSI_MAGENTA = "\033[35m"
    ANSI_CYAN = "\033[36m"
    ANSI_WHITE = "\033[37m"

    ANSI_BRIGHT_BLACK = "\033[30;1m"
    ANSI_BRIGHT_RED = "\033[31;1m"
    ANSI_BRIGHT_GREEN = "\033[32;1m"
    ANSI_BRIGHT_YELLOW = "\033[33;1m"
    ANSI_BRIGHT_BLUE = "\033[34;1m"
    ANSI_BRIGHT_MAGENTA = "\033[35;1m"
    ANSI_BRIGHT_CYAN = "\033[36;1m"
    ANSI_BRIGHT_WHITE = "\033[37;1m"

    @classmethod
    def apply_color_tags(cls, text):
        color_pattern = re.compile(r'\[(?P<color>\w+)\](?P<text>.*?)\[/\1\]', re.DOTALL)
        formatted_text = text

        for match in color_pattern.finditer(text):
            color_name = match.group('color').upper()
            if hasattr(cls, f'ANSI_{color_name}'):
                color_code = getattr(cls, f'ANSI_{color_name}')
                colored_text = color_code + match.group('text') + cls.ANSI_RESET
                formatted_text = formatted_text.replace(match.group(0), colored_text)

        return formatted_text

