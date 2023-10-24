from .cli import cli

from aiohttp.client_exceptions import ClientResponseError

try:
    cli()
except ClientResponseError as ex:
    print("Error:", ex.status, ex.message)
