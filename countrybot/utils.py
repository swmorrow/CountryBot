from typing import Literal
import discord
from requests import head
from datetime import datetime
from config import ICON

### Image Functions ###

def is_url(url: str) -> bool:
    """Checks if an image is a url (starts with http:// or https://)"""
    return url.startswith("http://") or url.startswith("https://")

def is_url_image(image_url: str) -> bool:
    """Checks if a url leads to an image"""
    try:
        image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp")
        r = head(image_url)
        return r.headers["content-type"] in image_formats
    except:
        return False

def embed_img_or_desc(embed: discord.Embed, img_type: Literal["thumbnail","image"], name: str, value: str) -> bool:
    """
    Takes a string input and tries to apply the specified function (ex, set_image).
    - If it is not a valid image, sets a description field.
    - If it is a url but not a valid image, sets a link field.
    - If it is a valid image, applies the specified embed set function.\n
    Returns `True` if it was a valid image, otherwise returns `False`.
    """
    value = value.strip()

    if not is_url(value):
        embed.add_field(name=f"{name} Description", value=value, inline=False)
        return False

    if is_url_image(value):
        if img_type == "thumbnail":
            embed.set_thumbnail(url=value)
            if not embed.thumbnail:
                embed.add_field(name=f"{name} Link", value=value, inline=False)
                return False

            return True

        elif img_type == "image":
            embed.set_image(url=value)
            if not embed.image:
                embed.add_field(name=f"{name} Link", value=value, inline=False)
                return False

            return True       

    embed.add_field(name=f"{name} Link", value=value, inline=False)
    return False

### Modal Functions ###

def children_to_embed(children, entity, user, embed: discord.Embed = None) -> discord.Embed:
    if embed:
        embed.clear_fields()
        embed.remove_image()
        embed.remove_thumbnail()
    else:
        embed = discord.Embed(
            title=children[0].value,
            description=children[1].value,
            color=discord.Color.blurple(),
            timestamp=datetime.now()
        )
    embed.set_footer(text=f"{entity} claim", icon_url=ICON)
    embed.set_author(name=user.display_name, icon_url=user.avatar.url)

    if len(children[2].value) > 0:
        embed.insert_field_at(index=1, name=children[2].label, value=children[2].value, inline=False)

    if len(children[3].value) > 0:
        if entity == "Country":
            embed_img_or_desc(embed, "thumbnail", children[3].label, children[3].value)
        else:
            embed.add_field(name=children[3].label, value=children[3].value, inline=False)

    if len(children[4].value) > 0:
        embed_img_or_desc(embed, "image", children[4].label, children[4].value)

    return embed