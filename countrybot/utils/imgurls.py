import discord
import numpy as np
from PIL import UnidentifiedImageError, Image
from time import process_time
from typing import Literal
import aiohttp
from countrybot.utils.excepts import InvalidAliasingError
from io import BytesIO

### EMBED URL FUNCTIONS ###

async def embed_img_or_desc(embed: discord.Embed, img_type: Literal["thumbnail","image"], name: str, value: str) -> bool:
    """
    Takes a string input and tries to apply the specified function (ex, set_image).
    - If it is not a valid image, sets a description field.
    - If it is a url but not a valid image, sets a link field.
    - If it is a valid image, applies the specified embed set function.\n
    Returns `True` if it was a valid image, otherwise returns `False`.
    """
    value = value.strip()

    async with aiohttp.ClientSession() as session:
        try:  
            image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp")
            async with session.head(value) as req:
                if req.content_type in image_formats:
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

        except aiohttp.InvalidURL:
            embed.add_field(name=f"{name} Description", value=value, inline=False)
            return False

    embed.add_field(name=f"{name} Link", value=value, inline=False)
    return False

### FLAGIFY FUNCTIONS ###

def _set_pixel(img: np.ndarray, x: int, y: int, val: int, channel: int = 3):
    """Sets"""
    corner_pixels = (
        img[len(img[0])//8-x][len(img[0])//8-y], # top left 
        img[-len(img[0])//8+x][len(img[0])//8-y], # top right 
        img[len(img[0])//8-x][-len(img[0])//8+y], # bottom left
        img[-len(img[0])//8+x][-len(img[0])//8+y] # bottom right
    )
    for pixel in corner_pixels:
        pixel[channel] = val

async def flagify_image(flag: discord.Attachment | str, aliasing: float, image_binary: BytesIO) -> Image:
    if aliasing < 0 or aliasing > 1:
        raise InvalidAliasingError

    if isinstance(flag, str):
        async with aiohttp.ClientSession() as session:
            image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp")
            async with session.head(flag) as req:
                if not req.content_type in image_formats:
                    raise UnidentifiedImageError
            
            async with session.get(flag) as req:
                raw_img = Image.open(BytesIO(await req.read()))

    else:
        raw_img = Image.open(BytesIO(await flag.read()))

    raw_img = raw_img.convert("RGBA")
    raw_img.putalpha(255)

    img = np.array(raw_img)

    t1_start = process_time() 

    img = np.array(raw_img)

    ONE_EIGHTHS_H = len(img)//8
    ONE_EIGHTHS_L = len(img[0])//8

    for y in range(ONE_EIGHTHS_H*2): 
        for x in range(ONE_EIGHTHS_L*2):
            rad = np.sqrt(y*y + x*x)
            try:
                # if x and y are both in the corner
                if rad >= ONE_EIGHTHS_L:
                    # if the pixels make up the border of the corner
                    if rad < ONE_EIGHTHS_L+aliasing and rad > ONE_EIGHTHS_L-aliasing:
                        aliased_opacity = 255-(rad-ONE_EIGHTHS_L)*255
                        _set_pixel(img, x, y, aliased_opacity) # set pixel to aliansed opacity
                    
                    # if the pixels are in the zone to be nmade transparent
                    elif not y > ONE_EIGHTHS_L and not x > ONE_EIGHTHS_L:
                        _set_pixel(img, x, y, 0) # make pixel transparent

                    else:
                        break

            except IndexError:
                pass # just in case

    # check if there are any pixels left on the sides
    residual_pixels = False

    if img[0][1][3] != 0 or img[1][0][3] != 0: # if there is a line at the top
        residual_pixels = True

    t1_stop = process_time()
    out_image = Image.fromarray(img)

    if residual_pixels: 
        out_image = out_image.crop((1, 1, len(img[0])-1, len(img)-1))
        
    print(f"Elapsed time during the whole program: {t1_stop-t1_start}s") 

    out_image.save(image_binary, 'PNG')
    image_binary.seek(0)