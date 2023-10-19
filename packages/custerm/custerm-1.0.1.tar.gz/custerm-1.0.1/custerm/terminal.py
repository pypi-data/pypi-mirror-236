from dataclasses import dataclass
from custerm.ansi import *
import re

@dataclass
class Terminal:
    @staticmethod
    def print(text: str, markdown=False):
        if markdown:
            text = Terminal.render_markdown(text)
        text = Color.apply_color_tags(text)  
        print(text)

    @staticmethod
    def render_markdown(text):
        patterns = [
            (r'^(#{1,6})\s+(?P<markdown_text>.+)', r'\033[1;36m\2\033[0m'),  # Headings
            (r'\*\*([\w\s]+)\*\*', r'\033[1m\1\033[0m'),  # Bold
            (r'__([\w\s]+)__', r'\033[4m\1\033[0m'),  # Underline
            (r'\*([\w\s]+)\*', r'\033[3m\1\033[0m'),  # Italics
            (r'-\s+([\w\s]+)', r'\033[1;32m• \1\033[0m'),  # List items
            (r'```', r'\033[1;30m'),  # Code blocks start
            (r'```(.+?)```', r'\033[1;30m\1\033[0m')  # Code blocks content
        ]

        in_code_block = False
        formatted_lines = []

        for line in text.split('\n'):
            if in_code_block:
                if "```" in line:
                    in_code_block = False
                    line = line + '\033[0m'
                else:
                    line = re.sub(r'\*\*|__|\*|_', '', line)  #
            else:
                for pattern, replace in patterns:
                    line = re.sub(pattern, replace, line)
                if "```" in line:
                    in_code_block = True

            formatted_lines.append(line)

        return '\n'.join(formatted_lines)
