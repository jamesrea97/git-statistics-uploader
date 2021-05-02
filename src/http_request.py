"""This module contains HTTP request logic"""
from dataclasses import dataclass

import aiohttp


@dataclass
class HttpResponse:
    url: str
    status: int
    response: str


async def get(url: str) -> HttpResponse:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                status = resp.status
                response = await resp.text()
                return HttpResponse(url=url,
                                    status=status,
                                    response=response)
    except Exception:  # TODO figure out the type of Exception
        return HttpResponse(url=url,
                            status=500,
                            response='Server Error')
