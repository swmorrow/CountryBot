import pickle, config
from countrybot.RPDate import DateNotSetError, RPDate

def load_rpdate() -> RPDate:
    """Loads saved RP date"""
    try:
        f = open(config.PICKLE_PATH, "rb")
        rpdate = pickle.load(f)
        f.close()
        return rpdate
        
    except FileNotFoundError:
        raise DateNotSetError

def save_rpdate(rpdate: RPDate) -> None:
    """Saves RP date"""
    f = open(config.PICKLE_PATH, "wb")
    pickle.dump(rpdate, f)
    f.close()
    
    if load_rpdate() != rpdate:
        raise pickle.PickleError
