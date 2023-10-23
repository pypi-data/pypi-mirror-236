import json

from fastapi.responses import HTMLResponse


class HXLocationResponse(HTMLResponse):
    """HTMX location redirection response."""

    def __init__(self, path: str, target: str | None = None) -> None:
        """HTMX location redirection response.

        Args:
            path (str): The path to redirect the location to.
            target (str | None, optional): The optional DOM target. Defaults to None.
        """
        headers = {"path": path}
        if target:
            headers["target"] = target
        self.headers = {"HX-Location": json.dumps(headers)}
        # FIXME: add the super call as well since Response() has an init method
