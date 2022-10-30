import discord
import numpy as np
import PIL.Image
import PIL
from time import process_time
from typing import Literal
import aiohttp
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

async def flagify_image(flag: discord.Attachment | str) -> PIL.Image:
    t1_start = process_time() 

    ALIASING = 0.7

    if isinstance(flag, str):
        async with aiohttp.ClientSession() as session:
            image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp")
            async with session.head(flag) as req:
                if not req.content_type in image_formats:
                    raise PIL.UnidentifiedImageError
            
            async with session.get(flag) as req:
                raw_img = PIL.Image.open(BytesIO(await req.read()))

    else:
        raw_img = PIL.Image.open(BytesIO(await flag.read()))

    raw_img = raw_img.convert("RGBA")
    raw_img.putalpha(255)

    if raw_img.size[0]*raw_img.size[1] > 8_000_000:
        raise PIL.Image.DecompressionBombError

    ONE_EIGHTHS_L = raw_img.size[0]//8
    ONE_EIGHTHS_H = raw_img.size[1]//8

    img = np.array(raw_img)

    # This can be optimized, however, it is currently sufficient since discord files must be below 8mb.
    for y in range(ONE_EIGHTHS_H*2): 
        for x in range(ONE_EIGHTHS_L*2):
            rad = np.sqrt(y*y + x*x)
            try:
                # if neither x nor y are in the corner, continue
                if rad < ONE_EIGHTHS_L:
                    continue

                corner_pixels = (
                    img[ONE_EIGHTHS_L-x][ONE_EIGHTHS_L-y], # top left 
                    img[-ONE_EIGHTHS_L+x][ONE_EIGHTHS_L-y], # top right 
                    img[ONE_EIGHTHS_L-x][-ONE_EIGHTHS_L+y], # bottom left
                    img[-ONE_EIGHTHS_L+x][-ONE_EIGHTHS_L+y] # bottom right
                )

                # if the pixels make up the border of the corner
                if rad < ONE_EIGHTHS_L+ALIASING and rad > ONE_EIGHTHS_L-ALIASING:
                    # Set the opacity proportional to how close the radius is to 1/8 the length of the image
                    opacity = 255-(rad-ONE_EIGHTHS_L)*255
                
                # if the pixels are in the zone to be made transparent
                elif y <= ONE_EIGHTHS_L and x <= ONE_EIGHTHS_L:
                    opacity = 0

                else: # the pixels are in the solid part of the corner, so continue to the next row
                    break

                for pixel in corner_pixels:
                    pixel[3] = opacity # idx 3 is the alpha channel

            except IndexError: # just in case
                print("Out of bounds in Flagify")

    # check if there are any pixels left on the sides
    residual_pixels = False

    if img[0][1][3] != 0 or img[1][0][3] != 0: # if there is a line at the top or on the side
        residual_pixels = True

    t1_stop = process_time()
    out_image = PIL.Image.fromarray(img)

    if residual_pixels: 
        out_image = out_image.crop((1, 1, len(img[0])-1, len(img)-1))
        
    print(f"Elapsed time to process image: {t1_stop-t1_start}s") 
    return out_image