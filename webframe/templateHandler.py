import re

HTML_PATH = 'templates/'
ERROR_HTML = 'webframe/'


class Template:
    def __init__(self, path) -> None:
        self.template_path = path


def parse_template(path):
    if '404' in path:
        with open(f"{ERROR_HTML}{path}", 'r') as file:
            html_content = file.read()
            return html_content
    try:
        with open(f"{HTML_PATH}{path}", 'r') as file:
            html_content = file.read()
            return html_content
    except FileNotFoundError:
        return "error"
