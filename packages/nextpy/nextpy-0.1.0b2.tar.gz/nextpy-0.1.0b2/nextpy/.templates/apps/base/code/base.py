"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from typing import Callable

import nextpy as xt

from .pages import dashboard_page, home_page, settings_page
from .sidebar import sidebar
from .styles import *


def template(main_content: Callable[[], xt.Component]) -> xt.Component:
    """The template for each page of the app.

    Args:
        main_content (Callable[[], xt.Component]): The main content of the page.

    Returns:
        xt.Component: The template for each page of the app.
    """
    menu_button = xt.box(
        xt.menu(
            xt.menu_button(
                xt.icon(
                    tag="hamburger",
                    size="4em",
                    color=text_color,
                ),
            ),
            xt.menu_list(
                xt.menu_item(xt.link("Home", href="/", width="100%")),
                xt.menu_divider(),
                xt.menu_item(
                    xt.link("About", href="https://github.com/dot-agent", width="100%")
                ),
                xt.menu_item(
                    xt.link("Contact", href="mailto:anurag@=dotagent.ai", width="100%")
                ),
            ),
        ),
        position="fixed",
        right="1.5em",
        top="1.5em",
        z_index="500",
    )

    return xt.hstack(
        sidebar(),
        main_content(),
        xt.spacer(),
        menu_button,
        align_items="flex-start",
    )


@xt.page("/")
@template
def home() -> xt.Component:
    """Home page.

    Returns:
        xt.Component: The home page.
    """
    return home_page()


@xt.page("/settings")
@template
def settings() -> xt.Component:
    """Settings page.

    Returns:
        xt.Component: The settings page.
    """
    return settings_page()


@xt.page("/dashboard")
@template
def dashboard() -> xt.Component:
    """Dashboard page.

    Returns:
        xt.Component: The dashboard page.
    """
    return dashboard_page()


# Add state and page to the app.
app = xt.App(style=base_style)
app.compile()
