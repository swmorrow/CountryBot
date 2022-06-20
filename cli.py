import fire
from countrybot.utils.io import (
    register,
    unregister,
    save_rpdate_channel,
    load_rpdate_channel,
    save_approve_channel,
    load_approve_channel,
    get_num_countries
)
from countrybot.utils.imgurls import (
    is_url,
    is_url_image
)

if __name__ == '__main__':
    fire.Fire()
