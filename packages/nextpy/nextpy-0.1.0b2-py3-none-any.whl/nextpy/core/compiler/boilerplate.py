"""Boilerplate to use in the nextpy compiler."""

from jinja2 import Environment, FileSystemLoader, Template

from nextpy import constants
from nextpy.utils.format import json_dumps


class NextpyJinjaEnvironment(Environment):
    """The boilerplate class for jinja environment."""

    def __init__(self) -> None:
        """Set default environment."""
        extensions = ["jinja2.ext.debug"]
        super().__init__(
            extensions=extensions,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.filters["json_dumps"] = json_dumps
        self.filters["react_setter"] = lambda state: f"set{state.capitalize()}"
        self.loader = FileSystemLoader(constants.Boilerplate.Dirs.JINJA_BOILERPLATE)
        self.globals["const"] = {
            "socket": constants.CompileVars.SOCKET,
            "result": constants.CompileVars.RESULT,
            "router": constants.CompileVars.ROUTER,
            "event_endpoint": constants.Endpoint.EVENT.name,
            "events": constants.CompileVars.EVENTS,
            "state": constants.CompileVars.STATE,
            "final": constants.CompileVars.FINAL,
            "processing": constants.CompileVars.PROCESSING,
            "initial_result": {
                constants.CompileVars.STATE: None,
                constants.CompileVars.EVENTS: [],
                constants.CompileVars.FINAL: True,
                constants.CompileVars.PROCESSING: False,
            },
            "color_mode": constants.ColorMode.NAME,
            "toggle_color_mode": constants.ColorMode.TOGGLE,
            "use_color_mode": constants.ColorMode.USE,
            "hydrate": constants.CompileVars.HYDRATE,
        }
    def get_boilerplate(self, name: str) -> Template:
        return self.get_template(name)


def get_boilerplate(name: str) -> Template:
    """Get render function that work with a boilerplate.

    Args:
        name: The boilerplate name. "/" is used as the path separator.

    Returns:
        A render function.
    """
    return NextpyJinjaEnvironment().get_boilerplate(name=name)


# Boilerplate for the Nextpy config file.
XTCONFIG = get_boilerplate("app/xtconfig.py.jinja2")

# Code to render a NextJS Document root.
DOCUMENT_ROOT = get_boilerplate("web/pages/_document.js.jinja2")

# Boilerplate for the theme file.
THEME = get_boilerplate("web/utils/theme.js.jinja2")

# Boilerplate for the context file.
CONTEXT = get_boilerplate("web/utils/context.js.jinja2")

# Boilerplate for Tailwind config.
TAILWIND_CONFIG = get_boilerplate("web/tailwind.config.js.jinja2")

# Boilerplate to render a component tag.
COMPONENT = get_boilerplate("web/pages/component.js.jinja2")

# Code to render a single NextJS page.
PAGE = get_boilerplate("web/pages/index.js.jinja2")

# Code to render the custom components page.
COMPONENTS = get_boilerplate("web/pages/custom_component.js.jinja2")

# Sitemap config file.
SITEMAP_CONFIG = "module.exports = {config}".format

# Code to render the root stylesheet.
STYLE = get_boilerplate("web/styles/styles.css.jinja2")

# Code that generate the package json file
PACKAGE_JSON = get_boilerplate("web/package.json.jinja2")
