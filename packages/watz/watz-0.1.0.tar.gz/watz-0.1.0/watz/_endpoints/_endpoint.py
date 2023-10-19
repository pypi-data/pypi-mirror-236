import time
import warnings

import httpx
import typing_extensions as tp
from pydantic import ValidationError

from .req_base import ReqBase
from .resp_base import RespBase, RespBytes

Req_T = tp.TypeVar("Req_T", bound=ReqBase)
Resp_T = tp.TypeVar("Resp_T", bound=tp.Union[RespBase, RespBytes])
Method_T = tp.TypeVar("Method_T", bound=tp.Literal["POST"])

CONN_WAIT_SECS = 0.5


class Endpoint(tp.Generic[Method_T, Req_T, Resp_T]):
    method: Method_T
    req_model: type[Req_T]
    resp_model: type[Resp_T]
    path: str

    def __init__(
        self,
        method: Method_T,
        path: str,
        req_model: type[Req_T],
        resp_model: type[Resp_T],
    ):
        path = path.strip()
        self.req_model = req_model
        self.resp_model = resp_model
        self.method = method.upper()
        self.path = path

    def call(self, session: httpx.Client, req: Req_T) -> Resp_T:
        resp = self._req(session, req)
        return self._parse(resp)

    def _req(
        self,
        session: httpx.Client,
        req: Req_T,
    ) -> httpx.Response:
        json_content = req.model_dump_json()
        # Pull out the files to pass in separately if needed:
        files = req._extract_files()

        for x in range(5):
            try:
                return session.request(
                    self.method,
                    self.path,
                    # When sending as multipart/form-data:
                    files=files,
                    data={"json": json_content} if files else None,
                    # When sending directly as json:
                    content=json_content if not files else None,
                    headers={"Content-Type": "application/json"} if not files else None,
                )
            except httpx.ConnectError:
                warnings.warn(
                    "Failed to connect to Watz API. Attempt {} of 5.".format(x + 1), stacklevel=3
                )
            time.sleep(CONN_WAIT_SECS)

        raise httpx.ConnectError("Failed to connect to Watz API after 5 attempts.")

    def _format_resp_data(self, resp: httpx.Response) -> tp.Any:
        try:
            return resp.json()
        except ValueError:
            return resp.content

    def _parse(self, resp: httpx.Response) -> Resp_T:
        if resp.status_code != 200:
            raise httpx.HTTPStatusError(
                "Unexpected status code from Watz API: {}\n{}".format(resp.status_code, resp.text),
                request=resp.request,
                response=resp,
            )

        try:
            # Check if json:
            if resp.headers.get("Content-Type", "").lower() == "application/json":
                # Pass the bytes directly into pydantic to try and avoid python decoding:
                return self.resp_model.model_validate_json(resp.content)
            elif issubclass(self.resp_model, RespBytes):
                # Used for e.g. zip file responses:
                return self.resp_model(root=resp.content)
            else:
                raise ValueError()
        except (ValidationError, ValueError) as e:
            raise ValueError(
                "Unexpected data structure from Watz API.\n{}".format(self._format_resp_data(resp))
            ) from e
