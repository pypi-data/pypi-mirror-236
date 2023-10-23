"""The home page of the app."""
import nextpy as xt

from ..styles import *


def home_page() -> xt.Component:
    """The UI for the home page.

    Returns:
        xt.Component: The UI for the home page.
    """
    return xt.box(
        xt.vstack(
            xt.heading(
                "Home",
                size="3em",
            ),
            xt.text(
                "Welcome to Nextpy!",
            ),
            xt.text(
                "You can use this template to get started with Nextpy.",
            ),
            style=template_content_style,
        ),
        style=template_page_style,
    )
