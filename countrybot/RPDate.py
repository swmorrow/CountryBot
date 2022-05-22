from datetime import date
from time import strptime
from typing import Union
import sqlite3

class RPDate:
    """Object containing RP date information.

            Attributes:
                start_date: In-RP beginning date
                sep: IRL ays per in-RP year. Defaults to 2.
                irl_start_date: Real-life RP beginning date. Defaults to today.
    """

    def __init__(self, start_date: str, sep: str = "2", irl_start_date: Union(str, date) = date.today()):
        self.start_date = strptime(start_date, "%d/%m/%Y")
        self.sep = float(sep)
        self.irl_start_date = strptime(irl_start_date, "%d/%m/%Y") if isinstance(irl_start_date, str) else irl_start_date

    def get_date(self) -> date:
        pass