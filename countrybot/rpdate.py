from datetime import date, datetime, timedelta
from countrybot.utils.excepts import InvalidDateError

class RPDate:
    """Object containing RP date information.

    Attributes
    ------------
    start_date: :class:`date`
        In-RP beginning date
    ticks: :class:`float`
        IRL days per in-RP year. Defaults to 2.
    irl_start_date: :class:`datetime`
        Date that the in-RP date was set. Used to calculate current in-RP date.
    """
 
    def __init__(self, year: int, month: int, day: int, ticks: float) -> None:
        try:
            self._start_date = date(year, month, day)
        except ValueError:
            raise InvalidDateError

        self._irl_start_date = datetime.now()
        self.ticks = ticks

    def __eq__(self, other) -> bool:
        return self.get_date() == other.get_date()

    def __str__(self) -> str:
        date = self.get_date()
        return date.strftime("%B %d, %Y")
 
    def get_date(self) -> date:
        """Returns the in-RP date."""
        irldelta = (datetime.now() - self._irl_start_date) / timedelta(days=1)
        rpdelta = (irldelta/self.ticks)*365.2425
        rp_date = self._start_date.toordinal()+rpdelta

        return date.fromordinal(int(rp_date))
