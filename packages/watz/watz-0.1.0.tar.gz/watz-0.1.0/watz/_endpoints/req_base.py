"""The shared base request model for all endpoints."""

import typing as tp

from pydantic import BaseModel


class ReqBase(BaseModel):
    """The base request model for all API endpoints."""

    def _extract_files(self) -> tp.Union[dict[str, bytes], None]:
        return None

    def _hydrate_files(self, files: dict[str, bytes]):
        pass
