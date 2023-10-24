import os
import click
import json as pyjson
import logging

from aiohttp import ClientSession, CookieJar
from datetime import datetime
from getpass import getpass
from html2text import html2text
from os import path
from typing import Any, AsyncGenerator, cast

from patreon_dl import api, http
from patreon_dl.data import Item, parse_included, reify_relationships_many, reify_relationships_one
from patreon_dl.decorators import async_command, pass_session
from patreon_dl.html import extract_images
from patreon_dl.output import print_table


Data = dict[str, Any]


# Tweak the Click context
# https://click.palletsprojects.com/en/8.1.x/api/#context
CONTEXT = dict(
    # Enable using environment variables to set options
    auto_envvar_prefix="PATREON_DL",
    # Add shorthand -h for invoking help
    help_option_names=["-h", "--help"],
    # Give help some more room (default is 80)
    max_content_width=100,
    # Always show default values for options
    show_default=True,
)


@click.group(context_settings=CONTEXT)
@click.option("--debug/--no-debug", default=False, help="Log debug info to stderr")
def cli(debug: bool):
    if debug:
        logging.basicConfig(level=logging.DEBUG)


@cli.command()
@click.argument("email")
@async_command
@pass_session
async def login(session: ClientSession, email: str):
    password = getpass("Password: ")
    await api.login(session, email, password)
    cookie_jar = cast(CookieJar, session.cookie_jar)
    http.save_cookie_jar(cookie_jar)
    click.echo("Logged in!")


@cli.command()
@click.option("--json", default=False, is_flag=True, help="Dump data to json")
@async_command
@pass_session
async def whoami(session: ClientSession, json: bool):
    response = await api.current_user(session)

    if json:
        click.echo(await response.text())
        return

    data = await response.json()
    click.echo(data["data"]["attributes"]["full_name"])
    click.echo(data["data"]["attributes"]["url"])


@cli.command()
@click.option("--json", default=False, is_flag=True, help="Dump data to json")
@async_command
@pass_session
async def pledges(session: ClientSession, json: bool):
    response = await api.pledges(session)
    data = await response.json()
    included = parse_included(data)
    pledges = reify_relationships_many(data["data"], included)

    if json:
        click.echo(pyjson.dumps(pledges))
        return

    if not pledges:
        click.echo("No pledges found")
        return

    headers = ["ID", "Slug", "Name"]
    rows: list[list[str]] = []
    for pledge in pledges:
        rows.append([
            pledge["relationships"]["campaign"]["id"],
            pledge["relationships"]["campaign"]["attributes"]["vanity"],
            pledge["relationships"]["campaign"]["attributes"]["name"]
        ])
    rows.sort(key=lambda r: r[1].lower())
    print_table(headers, rows)


@cli.command()
@click.option("--output-dir", "-o", help="Directory where to sync the files", default=".")
@click.option("--campaign", "-c", "campaign_names", help="Campaign to sync, can be used multiple times", multiple=True)
@async_command
@pass_session
async def sync(session: ClientSession, output_dir: str, campaign_names: tuple[str]):
    campaigns = await fetch_campaigns_by_id(session)
    if not campaign_names:
        campaign_names = campaigns.keys()

    for campaign_name in campaign_names:
        campaign = campaigns.get(campaign_name)
        if campaign:
            campaign_dir = path.join(output_dir, campaign["attributes"]["vanity"])
            async for post in generate_posts(session, campaign["id"]):
                await download_post(session, post, campaign_dir)
        else:
            click.secho(f"Campaign {campaign_name} not found", fg="red")


async def download_post(session: ClientSession, post: Item, campaign_dir: str):
    dttm = datetime.fromisoformat(post["attributes"]["published_at"])
    slug = post["attributes"]["patreon_url"].replace("/posts/", "")
    target_dir = path.join(campaign_dir, f'{dttm.strftime("%Y-%m-%d")}_{slug}')
    os.makedirs(target_dir, exist_ok=True)

    click.secho(target_dir, bold=True)

    # content.md
    # TODO: replace remote images with local ones
    # TODO: also save html?
    content = post["attributes"]["content"]
    content_md = html2text(content) if content else ""
    with open(path.join(target_dir, "content.md"), "w") as f:
        f.write(f'# {post["attributes"]["title"]}\n\n')
        f.write(content_md)

        if post["attributes"]["post_type"] == "poll":
            poll = post["relationships"]["poll"]
            f.write("\n\n# Poll\n\n")
            f.write(f'{poll["attributes"]["question_text"]}\n\n')
            for choice in poll["relationships"]["choices"]:
                f.write(f'* {choice["attributes"]["text_content"]} [{choice["attributes"]["num_responses"]}]\n')

    # thumbnail
    image = post["attributes"]["image"]
    if image:
        await http.download_file(session, image["url"], target_dir, default_filename="thumbnail.jpg")

    # images
    # TODO: make sure there are no overwrites between images and thumbnail
    # TODO: download in parallel
    if content:
        image_urls = extract_images(content)
        for url in image_urls:
            await http.download_file(session, url, target_dir)

    post_type = post["attributes"]["post_type"]
    match post_type:
        case "audio_file":
            url = post["attributes"]["post_file"]["url"]
            filename = post["attributes"]["post_file"]["name"]
            click.echo(f"{post_type} {filename}")
            await http.download_file(session, url, target_dir)
        case "video_embed":
            url = post["attributes"]["embed"]["url"]
            http.ytdlp_download(url, target_dir)
        case "video_external_file":
            # TODO: It's possible to get subs via m3u8 playlist which is linked
            # in: post["attributes"]["post_file"]["url"]
            url = post["attributes"]["post_file"]["download_url"]
            await http.download_file(session, url, target_dir)
        case "image_file":
            pass  # Image already downloaded
        case "poll":
            pass  # Poll already downloaded
        case "text_only":
            pass
        case _:
            click.secho(f"Unhandled post type: {post_type}", fg="red")


@cli.command()
@click.argument("campaign_name")
@click.option("--json", default=False, is_flag=True, help="Dump data to json")
@async_command
@pass_session
async def posts(session: ClientSession, campaign_name: str, json: bool):
    headers = ["Date", "Type", "Title"]
    table_data: list[list[str]] = []
    campaign = await fetch_campaign_by_name(session, campaign_name)
    async for post in generate_posts(session, campaign["id"]):
        dttm = datetime.fromisoformat(post["attributes"]["published_at"])
        date = dttm.strftime("%Y-%m-%d")
        title = post["attributes"]["title"]
        post_type = post["attributes"]["post_type"]
        table_data.append([date, post_type, title])
    print_table(headers, table_data)


async def fetch_pledges(session: ClientSession) -> list[Item]:
    response = await api.pledges(session)
    data = await response.json()
    included = parse_included(data)
    return reify_relationships_many(data["data"], included)


async def fetch_campaign_by_name(session: ClientSession, name: str) -> Item:
    campaigns = await fetch_campaigns_by_id(session)
    campaign = campaigns.get(name.lower())
    if not campaign:
        click.secho(f"Campaign '{name}' not found.\n", fg="red")
        click.echo("Exisitng campaigns:")
        for name in sorted(campaigns.keys()):
            click.echo(f" * {name}")
        raise click.Abort()
    return campaign


async def fetch_campaigns_by_id(session: ClientSession) -> dict[str, Item]:
    pledges = await fetch_pledges(session)
    campaigns: dict[str, Item] = dict()
    for pledge in pledges:
        campaign = pledge["relationships"]["campaign"]
        vanity = campaign["attributes"]["vanity"].lower()
        campaigns[vanity] = campaign
    return campaigns


async def generate_posts(session: ClientSession, campaign_id: str) -> AsyncGenerator[Item, None]:
    async for data in api.posts_generator(session, campaign_id):
        included = parse_included(data)
        reified = reify_relationships_many(data["data"], included)
        for post in reified:
            if post["relationships"]["poll"]:
                post["relationships"]["poll"] = reify_relationships_one(post["relationships"]["poll"], included)
            yield post
