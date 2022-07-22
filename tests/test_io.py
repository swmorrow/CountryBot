import unittest
import countrybot.utils.io as io
from countrybot.rpdate import RPDate
from countrybot.utils.excepts import DateNotSetError, ChannelNotSetError

NUM_TESTS = 3

class TestIOMethods(unittest.TestCase):

    def test_register(self): 
        old_guilds = io.get_guilds()
        io.register(1)
        new_guilds = io.get_guilds()
        self.assertEqual(set(new_guilds), set(old_guilds + [1]), "Failed to register")

        io.unregister(1)
        new_guilds = io.get_guilds()
        self.assertEqual(set(old_guilds), set(new_guilds), "Failed to unregister")

    def test_rpdate_io(self): 
        io.register(2)
        with self.assertRaises(DateNotSetError):
            io.load_rpdate(2)

        test_rpdate = RPDate(1000, 1, 1, 2)
        io.save_rpdate(test_rpdate, 2)
        loaded_rpdate = io.load_rpdate(2)
        self.assertIsNotNone(loaded_rpdate)

        self.assertEqual(loaded_rpdate, test_rpdate)

        io.unregister(2)

    def test_rpdate_channel_io(self):
        io.register(3)
        with self.assertRaises(ChannelNotSetError):
            io.load_rpdate_channel(3)

        test_channel = 1
        io.save_rpdate_channel(test_channel, 3)
        loaded_channel = io.load_rpdate_channel(3)
        self.assertIsNotNone(loaded_channel)

        self.assertEqual(loaded_channel, test_channel)

        io.unregister(3)

    def test_approve_channel_io(self):
        io.register(4)
        with self.assertRaises(ChannelNotSetError):
            io.load_approve_channel(4)

        test_channel = 1
        io.save_approve_channel(test_channel, 4)
        loaded_channel = io.load_approve_channel(4)
        self.assertIsNotNone(loaded_channel)

        self.assertEqual(loaded_channel, test_channel)

        io.unregister(4)
    
    @classmethod
    def tearDownClass(cls):
        for i in range(1, NUM_TESTS+1):
            io.unregister(i)

if __name__ == '__main__':
    unittest.main()