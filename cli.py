import fire
from countrybot.utils.io import (
    get_guilds,
    register,
    unregister,
    save_rpdate_channel,
    load_rpdate_channel,
    save_approve_channel,
    load_approve_channel,
)
from countrybot.utils.imgurls import (
    is_url,
    is_url_image
)

if __name__ == '__main__':
    fire.Fire()
