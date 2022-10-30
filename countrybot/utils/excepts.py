class ChannelNotSetError(Exception):
    def __init__(self, channel: str, *args, **kwargs):
        self.channel = channel
        super().__init__(*args, **kwargs)

class DateNotSetError(Exception):
    pass

class InvalidDateError(ValueError):
    pass

class RPDateNotPostedError(Exception):
    pass

class ImageTooSmallError(Exception):
    pass