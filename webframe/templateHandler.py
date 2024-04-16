HTML_PATH = 'templates/'
ERROR_HTML = 'webframe/'


class Template:
    def __init__(self, path) -> None:
        self.template_path = path


def parse_template(path, status_code):
    if status_code == 400 or status_code == 404:
        with open(f"{ERROR_HTML}{path}", 'r') as file:
            html_content = file.read()
            return html_content, status_code
    try:
        with open(f"{HTML_PATH}{path}", 'r') as file:
            html_content = file.read()
            return html_content, status_code
    except FileNotFoundError:
        return "error"
