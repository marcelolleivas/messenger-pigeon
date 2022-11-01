import jinja2
from jinja2 import select_autoescape

SEARCH_PATH = "../templates"
TEMPLATE_FILE = "simple_email.html"


def template_render(title, message):
    template_loader = jinja2.FileSystemLoader(searchpath=SEARCH_PATH)
    template_env = jinja2.Environment(
        loader=template_loader, autoescape=select_autoescape(["html"])
    )
    template = template_env.get_template(TEMPLATE_FILE)

    data = {"title": title, "message": message}

    return template.render(data)
