"""The dashboard page for the template."""
import nextpy as xt

from ..styles import *


def dashboard_page() -> xt.Component:
    """The UI for the dashboard page.

    Returns:
        xt.Component: The UI for the dashboard page.
    """
    return xt.box(
        xt.vstack(
            xt.heading(
                "Dashboard",
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
