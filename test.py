
import unittest

from hashaddressmap import hash_address_map


class TestAll(unittest.TestCase):
    def setUp(self):
        pass

    def testHashAddressMap(self):
        pairs = [["foo@bar.com", "foo@bar.com"],
                 ["foo#test@bar.com", "foo@bar.com"]]


        for addr, expected in pairs:
            mapped = hash_address_map(addr)
            msg = "'{}' != '{}'".format(mapped, expected)
            assert mapped == expected, msg
