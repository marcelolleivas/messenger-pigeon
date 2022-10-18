import jinja2


def template_render(search_path, template_file):
    template_loader = jinja2.FileSystemLoader(searchpath=search_path)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)
    return template.render()
