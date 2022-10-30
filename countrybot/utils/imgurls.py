import discord
import numpy as np
import PIL.Image # must import PIL.Image before PIL
import PIL
import aiohttp

from time import process_time
from typing import Literal
from io import BytesIO
from .excepts import ImageTooSmallError

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

    if not value.startswith(("http", "https")):
        embed.add_field(name=name, value=value, inline=False)
        return False

    if img_type == "thumbnail":
        embed.set_thumbnail(url=value)
        if embed.thumbnail is discord.Embed.Empty: # failed to set thumbnail, so put it in a field as a link instead
            embed.add_field(name=name, value=value, inline=False)
            return False

        return True

    # img_type must be "image" if it isnt "thumbnail"
    embed.set_image(url=value)
    if embed.image is discord.Embed.Empty: # failed to set image, so put it in a field as a link instead
        embed.add_field(name=name, value=value, inline=False)
        return False

    return True       

### FLAGIFY FUNCTIONS ###

async def flagify_image(flag: discord.Attachment | str) -> BytesIO:
    # This might take up too much memory 
    t1_start = process_time() 

    ALIASING = 0.7

    if isinstance(flag, str):
        async with aiohttp.ClientSession() as session:
            image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp")

            async with session.head(flag) as req:
                if not req.content_type in image_formats:
                    raise PIL.UnidentifiedImageError

            async with session.get(flag) as req:
                try:   
                    req_img = await req.read()

                except aiohttp.ClientPayloadError: # apparently this is incredibly rare, will deal with it if it turns out to not be rare
                    print("uh oh, ClientPayloadError in flagify")
                    raise PIL.UnidentifiedImageError

                raw_img = PIL.Image.open(BytesIO(req_img))

    else:
        raw_img = PIL.Image.open(BytesIO(await flag.read()))

    raw_img = raw_img.convert("RGBA")
    raw_img.putalpha(255)

    ONE_EIGHTHS_L = raw_img.size[0]//8
    ONE_EIGHTHS_H = raw_img.size[1]//8

    if ONE_EIGHTHS_L < 5 or ONE_EIGHTHS_H < 5:
        raise ImageTooSmallError

    img = np.array(raw_img)

    if img.size > 40_000_000:
        raise PIL.Image.DecompressionBombError

    # TODO: Optimize this more
    # We want the corners of the image to be semicircles with radii image_length/8
    # So, iterate through the pixels (denoted (x, y)) starting from the top left.
    # If the radius of (x, y) is greater than image_length/8, make them transparent for all corners (since it is symmetrical)
    # If the radius of (x, y) is approximately equal to image_length/8, make the pixels' opacity proportional to how close the radius is to image_length/8.
    # This makes the image aliased, thus making it prettier.
    # If none of the above are true, break to the next row of y pixels.
    for y in range(ONE_EIGHTHS_H*2): 
        for x in range(ONE_EIGHTHS_L*2):
            rad = np.sqrt(y*y + x*x)
            try:
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

                else: # x must be greater than ONE_EIGHTHS_L now, so continue to the next row of pixels
                    break

                for pixel in corner_pixels:
                    pixel[3] = opacity # idx 3 is the alpha channel
            except IndexError: # just in case
                print("Out of bounds in Flagify")

    out_image = PIL.Image.fromarray(img)

    if img[0][1][3] != 0 or img[1][0][3] != 0: # if there is a line at the top or on the side
        out_image = out_image.crop((1, 1, len(img[0])-1, len(img)-1))

    output = BytesIO()

    out_image.save(output, format="PNG")
    output_size = output.tell() # cursor is on the last byte after saving
    
    if output_size >= 7_990_000: # less than 8mb for leeway
        scale_factor = 7_990_000 / output_size # scale by how much bigger it is than the max (with some leeway)

        out_image = out_image.resize((
            int(len(img[0]) * scale_factor),
            int(len(img) * scale_factor)
        ))

        output.close()
        output = BytesIO()
        out_image.save(output, format="PNG")

    output.seek(0)

    t1_stop = process_time()
        
    print(f"Elapsed time to process image: {t1_stop-t1_start}s") 
    return output