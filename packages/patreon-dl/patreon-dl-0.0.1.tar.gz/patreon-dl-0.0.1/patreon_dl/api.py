from aiohttp import ClientResponse, ClientSession
from typing import Any, AsyncGenerator
from urllib.parse import urlencode


async def login(session: ClientSession, email: str, password: str):
    url = "https://www.patreon.com/api/login"

    params = {
        "include": "campaign,user_location",
        "json-api-version": "1.0",
    }

    payload = {
        "data": {
            "attributes": {
                "email": email,
                "password": password
            },
            "relationships": {},
            "type": "user"
        },
        "meta": {
            "redirect_target": "https://www.patreon.com/home"
        }
    }

    async with session.post(url, params=params, json=payload) as response:
        response.raise_for_status()
        return await response.json()


async def current_user(session: ClientSession) -> ClientResponse:
    url = "https://www.patreon.com/api/current_user"

    params = {
        "include": ",".join([
            "pledges.creator.campaign.null",
            "pledges.campaign.null",
            "follows.followed.campaign.null",
        ]),
        "fields[user]": ",".join([
            "image_url",
            "full_name",
            "url",
            "social_connections",
        ]),
        "fields[campaign]": ",".join([
            # "avatar_photo_image_urls",
            # "avatar_photo_url",
            "creation_name",
            "pay_per_name",
            "is_monthly",
            "is_nsfw",
            "name",
            "url",
        ]),
        "fields[pledge]": ",".join([
            "amount_cents",
            "cadence",
        ])
    }

    async with session.get(url, params=params) as response:
        response.raise_for_status()
        await response.read()
        return response


async def pledges(session: ClientSession):
    url = "https://www.patreon.com/api/pledges"

    params = {
        "include": ["address,campaign,campaign.rewards,reward,reward.items,card,most_recent_pledge_charge_txn,reward.items.reward_item_configuration,reward.items.merch_custom_variants,reward.items.merch_custom_variants.item,reward.items.merch_custom_variants.merch_product_variant"],
        "fields[address]": ["id,addressee,line_1,line_2,city,state,postal_code,country,phone_number"],
        "fields[campaign]": ["avatar_photo_url,annual_pledging_enabled,cover_photo_url,is_monthly,is_non_profit,is_active,name,pay_per_name,pledge_url,published_at,url,vanity"],
        "fields[user]": ["thumb_url,url,full_name"],
        "fields[pledge]": ["amount_cents,currency,pledge_cap_cents,cadence,created_at,has_shipping_address,is_paused,status,next_charge_date"],
        "fields[reward]": ["id,amount_cents,description,requires_shipping,title,unpublished_at"],
        "fields[reward-item]": ["id,title,description,patron_can_select_size,requires_shipping,item_type,is_published,is_ended,ended_at,reward_item_configuration"],
        "fields[merch-custom-variant]": ["id,item_id"],
        "fields[merch-product-variant]": ["id,color,size_code"],
        "fields[txn]": ["succeeded_at,failed_at"],
        "fields[card]": ["number,card_type,merchant_name,failed_payment_type,expiration_date,full_name"],
        "json-api-use-default-includes": ["false"],
        "json-api-version": ["1.0"]
    }

    async with session.get(url, params=params) as response:
        response.raise_for_status()
        await response.read()
        return response


async def posts(session: ClientSession, campaign_id: str) -> ClientResponse:
    url = posts_url(campaign_id)
    async with session.get(url) as response:
        response.raise_for_status()
        await response.read()
        return response


async def posts_generator(session: ClientSession, campaign_id: str) -> AsyncGenerator[Any, None]:
    url = posts_url(campaign_id)
    while url:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            yield data
            url = data.get("links", {}).get("next")


def posts_url(campaign_id: str):
    url = "https://www.patreon.com/api/posts"

    params = {
        "include": ",".join([
            "campaign",
            "access_rules",
            "attachments",
            "audio",
            "audio_preview.null",
            "images",
            "media",
            "native_video_insights",
            "poll.choices",
            "poll.current_user_responses.user",
            "poll.current_user_responses.choice",
            "poll.current_user_responses.poll",
            "user",
            "user_defined_tags",
            "ti_checks"
        ]),
        "fields[campaign]": ",".join([
            "currency",
            "show_audio_post_download_links",
            "avatar_photo_url",
            "avatar_photo_image_urls",
            "earnings_visibility",
            "is_nsfw",
            "is_monthly",
            "name",
            "url",
        ]),
        "fields[post]": ",".join([
            "change_visibility_at",
            "comment_count",
            "commenter_count",
            "content",
            "current_user_can_comment",
            "current_user_can_delete",
            "current_user_can_report",
            "current_user_can_view",
            "current_user_comment_disallowed_reason",
            "current_user_has_liked",
            "embed",
            "image",
            "impression_count",
            "insights_last_updated_at",
            "is_paid",
            "like_count",
            "meta_image_url",
            "min_cents_pledged_to_view",
            "post_file",
            "post_metadata",
            "published_at",
            "patreon_url",
            "post_type",
            "pledge_url",
            "preview_asset_type",
            "thumbnail",
            "thumbnail_url",
            "teaser_text",
            "title",
            "upgrade_url",
            "url",
            "was_posted_by_campaign_owner",
            "has_ti_violation",
            "moderation_status",
            "post_level_suspension_removal_date",
            "pls_one_liners_by_category",
            "video_preview",
            "view_count",
        ]),
        "fields[post_tag]": ",".join([
            "tag_type",
            "value",
        ]),
        "fields[user]": ",".join([
            "image_url",
            "full_name",
            "url",
        ]),
        "fields[access_rule]": ",".join([
            "access_rule_type",
            "amount_cents",
        ]),
        "fields[media]": ",".join([
            "id",
            "image_urls",
            "download_url",
            "metadata",
            "file_name",
        ]),
        "fields[native_video_insights]": ",".join([
            "average_view_duration",
            "average_view_pct",
            "has_preview",
            "id",
            "last_updated_at",
            "num_views",
            "preview_views",
            "video_duration",
        ]),
        "filter[campaign_id]": campaign_id,
        "filter[contains_exclusive_posts]": "true",
        "filter[is_draft]": "false",
        "sort": "-published_at",
        "json-api-version": "1.0",
    }

    return f"{url}?{urlencode(params)}"
