import zlib
from typing import Awaitable, Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute


class CRC32Route(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Awaitable[Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            crc32 = zlib.crc32(response.body)
            response.headers["X-Body-CRC32"] = str(crc32)
            return response

        return custom_route_handler
