from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Token


def _get_kwargs(
    *,
    user: str,
    password: str,
    client_id: Optional[str] = None,
    session_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    headers = {}

    if client_id:
        headers["X-Client-ID"] = client_id
    if session_id:
        headers["X-Session-ID"] = session_id
    if request_id:
        headers["X-Request-ID"] = request_id

    return {
        "method": "POST",
        "url": "/token",
        "auth": (user, password),
        "headers": headers,
    }


def _build_response(response: httpx.Response) -> Token:
    if response.status_code == HTTPStatus.OK:
        return Token(**response.json())
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError(response.url, response.status_code, response.content, response.headers)
    else:
        raise ResponseError(response.url, response.status_code, response.content, response.headers)


def sync(
    client: httpx.Client,
    *,
    user: str,
    password: str,
    client_id: Optional[str] = None,
    session_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Token:
    kwargs = _get_kwargs(
        user=user, password=password, client_id=client_id, session_id=session_id, request_id=request_id
    )
    response = client.request(**kwargs)
    return _build_response(response)


async def asyncio(
    client: httpx.AsyncClient,
    *,
    user: str,
    password: str,
    client_id: Optional[str] = None,
    session_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Token:
    kwargs = _get_kwargs(
        user=user, password=password, client_id=client_id, session_id=session_id, request_id=request_id
    )
    response = await client.request(**kwargs)
    return _build_response(response)
