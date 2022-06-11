import discord
from requests import head
from typing import Callable

### Image Functions ###

def is_url(url: str) -> bool:
    """Checks if an image is a url (starts with http:// or https://)"""
    return url.startswith("http://") or url.startswith("https://")

def is_url_image(image_url: str) -> bool:
    """Checks if a url leads to an image"""
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
    r = head(image_url)
    return r.headers["content-type"] in image_formats

def embed_img_or_desc(embed: discord.Embed, set_fn, name: str, value: str) -> bool:
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
        set_fn(url=value)
        return True

    embed.add_field(name=f"{name} Link", value=value, inline=False)
    return True