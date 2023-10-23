"""Base state for the app."""

import nextpy as xt


class State(xt.State):
    """State for the app."""

    @xt.var
    def origin_url(self) -> str:
        """Get the url of the current page.

        Returns:
            str: The url of the current page.
        """
        return self.router_data.get("asPath", "")
