from datetime import date, datetime, timedelta
from time import strptime
from locale import setlocale, LC_ALL
import config

class RPDate:
    """Object containing RP date information.

    Attributes
    ------------
    start_date: :class:`date`
        In-RP beginning date
    sep: :class:`float`
        IRL days per in-RP year. Defaults to 2.
    irl_start_date: :class:`datetime`
        Date that the in-RP date was set. Used to calculate current in-RP date.
    """

    def __init__(self, raw_date: str, sep: float = 2) -> None:
        setlocale(LC_ALL, config.LOCALE)
        raw_date = strptime(raw_date, "%x")

        self.start_date = date(raw_date.tm_year, raw_date.tm_mon, raw_date.tm_mday)
        self.sep = sep
        self.irl_start_date = datetime.now()
    
    def __eq__(self, other) -> bool:
        return self.get_date() == other.get_date()

    def __str__(self) -> str:
        date = self.get_date()
        return date.strftime("%B %d, %Y")
 
    def get_date(self) -> date:
        irldelta = (datetime.now() - self.irl_start_date) / timedelta(days=1) # convert timedelta to floating point days WHY DO YOU NOT WORKKKKKKKKK
        rpdelta = (irldelta/self.sep)*365.2425
        rp_date = self.start_date.toordinal()+rpdelta
        return date.fromordinal(int(rp_date))

class DateNotSetError(Exception):
    pass