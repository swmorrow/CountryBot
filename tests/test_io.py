import unittest
import countrybot.utils.io as io
from countrybot.rpdate import RPDate, DateNotSetError

class TestIOMethods(unittest.TestCase):

    def test_register(self): 
        old_guilds = io.get_guilds()
        io.register(1)
        new_guilds = io.get_guilds()
        self.assertNotEqual(old_guilds, new_guilds, "Failed to register")

        io.unregister(1)
        new_guilds = io.get_guilds()
        self.assertEqual(old_guilds, new_guilds, "Failed to unregister")

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

    # TODO: Add more tests

if __name__ == '__main__': # TODO: Set up test database
    unittest.main()