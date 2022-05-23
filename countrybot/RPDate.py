from datetime import date, datetime, timedelta
from time import strptime
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

    def __init__(self, year: int, month: int, day: int, sep: float) -> None:

        self.start_date = date(year, month, day)
        self.sep = sep
        self.irl_start_date = datetime.now()
    
    def __eq__(self, other) -> bool:
        return self.get_date() == other.get_date()

    def __str__(self) -> str:
        date = self.get_date()
        return date.strftime("%B %d, %Y")
 
    def get_date(self) -> date:
        irldelta = (datetime.now() - self.irl_start_date) / timedelta(days=1)
        rpdelta = (irldelta/self.sep)*365.2425
        rp_date = self.start_date.toordinal()+rpdelta
        return date.fromordinal(int(rp_date))

class DateNotSetError(Exception):
    pass