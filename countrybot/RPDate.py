from datetime import date
from time import strptime
import locale

class RPDate:
    """Object containing RP date information.

            Attributes:
                start_date: In-RP beginning date
                sep: IRL ays per in-RP year. Defaults to 2.
                irl_start_date: Real-life RP beginning date. Defaults to today. (Outdated but im tiiired)
    """

    def __init__(self, raw_date: str, sep: float = 2):
        locale.setlocale(locale.LC_ALL, 'en_CA')
        raw_date = strptime(raw_date, "%x")
        self.start_date = date(raw_date.tm_year, raw_date.tm_mon, raw_date.tm_mday)
        self.sep = sep
        self.irl_start_date = date.today()
    
    def __eq__(self, other):
        return self.get_date() == other.get_date()

    def __str__(self):
        date = self.get_date()
        return date.strftime("%B %d, %Y")
 
    def get_date(self) -> date:
        #TODO: Calculate the actual RP date
        return self.start_date

class DateNotSetError(Exception):
    pass