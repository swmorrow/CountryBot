import unittest
import countrybot.utils.io as io
import datetime as dt
from countrybot.rpdate import RPDate
from countrybot.utils.excepts import DateNotSetError, ChannelNotSetError, RPDateNotPostedError

class TestIOMethods(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        self.current_test = 0
        super().__init__(*args, **kwargs)

    async def test_register(self): 
        self.current_test = 1

        old_guilds = await io.get_guilds()
        await io.register(self.current_test)

        new_guilds = await io.get_guilds()
        self.assertEqual(set(new_guilds), set(old_guilds + [self.current_test]), "Failed to register")

        await io.unregister(self.current_test)
        new_guilds = await io.get_guilds()

        self.assertEqual(set(old_guilds), set(new_guilds), "Failed to unregister")

    async def test_rpdate_io(self): 
        self.current_test = 2

        await io.register(self.current_test)
        with self.assertRaises(DateNotSetError):
            await io.load_rpdate(self.current_test)

        test_rpdate = RPDate(1000, 1, 1, 2)
        await io.save_rpdate(test_rpdate, self.current_test)

        loaded_rpdate = await io.load_rpdate(self.current_test)
        self.assertIsNotNone(loaded_rpdate)

        self.assertEqual(loaded_rpdate, test_rpdate)

        await io.unregister(self.current_test)

    async def test_rpdate_channel_io(self):
        self.current_test = 3

        await io.register(self.current_test)
        with self.assertRaises(ChannelNotSetError):
            await io.load_rpdate_channel(self.current_test)

        test_channel = 1
        await io.save_rpdate_channel(test_channel, self.current_test)
        loaded_channel = await io.load_rpdate_channel(self.current_test)
        self.assertIsNotNone(loaded_channel)

        self.assertEqual(loaded_channel, test_channel)

        await io.unregister(self.current_test)

    async def test_approve_channel_io(self):
        self.current_test = 4

        await io.register(self.current_test)
        with self.assertRaises(ChannelNotSetError):
            await io.load_approve_channel(self.current_test)

        test_channel = 1
        await io.save_approve_channel(test_channel, self.current_test)
        loaded_channel = await io.load_approve_channel(self.current_test)
        self.assertIsNotNone(loaded_channel)

        self.assertEqual(loaded_channel, test_channel)

        await io.unregister(self.current_test)

    async def test_last_rpdate_posting_io(self):
        self.current_test = 5

        await io.register(self.current_test)

        with self.assertRaises(RPDateNotPostedError):
            await io.load_last_rpdate_posting(self.current_test)

        date = dt.datetime.now()
        await io.save_last_rpdate_posting(date, self.current_test)
        
        self.assertEqual(await io.load_last_rpdate_posting(self.current_test), date)

        await io.unregister(self.current_test)

    async def asyncTearDown(self):
        await io.unregister(self.current_test)

if __name__ == '__main__':
    unittest.main()