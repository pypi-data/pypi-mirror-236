import os
import typing as tp

import httpx

AUTH_HEADER = "X-API-KEY"
ENV_SECRET_NAME = "WATZ_SECRET"  # nosec


class ClientBase:
    version: int

    _base: httpx.URL
    _session: httpx.Client

    def __init__(
        self,
        base: str,
        secret: tp.Optional[str] = None,
        version: int = 1,
    ):
        self.version = version
        self._base = httpx.URL("{}/api/v{}".format(base.strip().strip("/"), self.version))

        if secret is not None:
            pass
        elif ENV_SECRET_NAME in os.environ:
            secret = os.environ[ENV_SECRET_NAME]
        else:
            raise ValueError(
                "No secret/api-key provided. Please provide a secret or set the '{}' environment variable.".format(
                    ENV_SECRET_NAME
                )
            )

        self._session = httpx.Client(base_url=self._base, headers={AUTH_HEADER: secret})
