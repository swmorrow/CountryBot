import pickle
from countrybot.RPDate import DateNotSetError, RPDate

def load_rpdate() -> RPDate:
    """Loads saved RP date"""
    try:
        f = open("RPDate.pickle", "rb") # RPDate.pickle not tracked by git
        rpdate = pickle.load(f)
        f.close()
        return rpdate
    except FileNotFoundError:
        raise DateNotSetError

def save_rpdate(rpdate: RPDate) -> None:
    """Saves RP date"""
    f = open("RPDate.pickle", "wb")
    pickle.dump(rpdate, f)
    f.close()