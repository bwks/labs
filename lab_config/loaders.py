from jinja2 import Environment, FileSystemLoader


def render_from_template(
        template_name, template_directory, trim_blocks=True, lstrip_blocks=True, **kwargs):
    """
    Render jinja template
    """
    loader = FileSystemLoader(template_directory)
    env = Environment(loader=loader, trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks)

    template = env.get_template(template_name)
    return template.render(**kwargs)
