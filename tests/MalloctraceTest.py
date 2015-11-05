import unittest
import os, sys
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from malloctrace.malloctrace import Malloctrace

class MallocTest(unittest.TestCase):
    """Unit test cases for Malloctrace"""
    maxDiff = None

    def setUp(self):
        self.filename = "tests/malloctrace.out"
        self.malloctest = Malloctrace(self.filename)
        self.malloctest.process_file()

    def test_malloc(self):
        address_range_test_list = [('0x7f7dbc274010', '0x7f7dbc874010'), ('0x7f7dbbc73010', '0x7f7dbc273010'),
        ('0x7f7dbac71010', '0x7f7dbb271010'), ('0x1f30010', '0x1f31410'), ('0x1f31420', '0x1f32810'),
        ('0x1f32820', '0x1f401f8'), ('0x7f7dba921010', '0x7f7dbab09490'), ('0x7f7dba738010', '0x7f7dba920518'),
        ('0x7f7dba6f7010', '0x7f7dba737014'), ('0x1f31420', '0x1f32810'), ('0x1f32820', '0x1f422b0'),
        ('0x1f422c0', '0x212a740'), ('0x1f31420', '0x1f32810'), ('0x1f32820', '0x1f401f8'),
        ('0x7f7db93fb010', '0x7f7db96a6990'), ('0x7f7db914f010', '0x7f7db93faa18'), ('0x1f40200', '0x1f80204'),
        ('0x1f31420', '0x1f32810'), ('0x1f32820', '0x1f422b0'), ('0x1f422c0', '0x21edc40'), ('0x1f31420', '0x1f32810'),
        ('0x1f32820', '0x1f401f8'), ('0x7f7db9338010', '0x7f7db96a6e90'), ('0x7f7db8fc9010', '0x7f7db9337f18'),
        ('0x1f40200', '0x1f80204'), ('0x1f31420', '0x1f32810'), ('0x1f32820', '0x1f422b0'), ('0x1f422c0', '0x22b1140')]
        self.assertListEqual(address_range_test_list,self.malloctest.address_range_list)


if __name__ == '__main__':
    unittest.main()
