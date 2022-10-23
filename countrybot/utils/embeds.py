import discord
from datetime import datetime
from countrybot.utils.imgurls import embed_img_or_desc
from countrybot.configparser import ICON

def msg_embed(msg: str, title: str = None) -> discord.Embed:
    """Converts message to default embed"""
    return discord.Embed(
        title=title,
        color=discord.Color.blurple(),
        description=msg
    )
def error_embed(msg: str, title: str = "Error") -> discord.Embed:
    """Converts message to error embed"""
    return discord.Embed(
        title=":no_entry:  " + title,
        color=discord.Color.brand_red(),
        description=msg
    )

def success_embed(msg: str, title: str = "Success") -> discord.Embed:
    """Converts message to success embed"""
    return discord.Embed(
        title=":white_check_mark:  " + title,
        color=discord.Color.green(),
        description=msg
    )

def warning_embed(msg: str, title: str = "Warning") -> discord.Embed:
    """Converts message to warning embed"""
    return discord.Embed(
        title=":information_source:  " + title,
        color=discord.Color.yellow(),
        description=msg
    )

async def children_to_embed(children, entity, user, embed: discord.Embed = None) -> discord.Embed:
    """Converts list of claim modal children to embed"""
    if embed:
        embed.clear_fields()
        embed.remove_image()
        embed.remove_thumbnail()
    else:
        embed = discord.Embed(
            color=discord.Color.blurple(),
            timestamp=datetime.now()
        )

    embed.title = children[0].value
    embed.description = children[1].value
    embed.set_footer(text=f"{entity.removesuffix(' claim')} claim", icon_url=ICON)
    embed.set_author(name=user.display_name, icon_url=user.avatar.url)

    if len(children[2].value) > 0:
        embed.insert_field_at(index=1, name=children[2].label, value=children[2].value, inline=False)

    if len(children[3].value) > 0:
        if entity == "Country":
            await embed_img_or_desc(embed, "thumbnail", children[3].label, children[3].value)
        else:
            embed.add_field(name=children[3].label, value=children[3].value, inline=False)

    if len(children[4].value) > 0:
        await embed_img_or_desc(embed, "image", children[4].label, children[4].value)

    return embed