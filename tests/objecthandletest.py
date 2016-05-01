import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__ + "/..")))
from goaway.objecthandle import ObjectHandle
import mock

from goaway.objecthandle import ObjectHandle


class ObjectHandleTest(unittest.TestCase):
    def setUp(self):
        self.name = "abc"
        self.store = mock.MagicMock()
        self.obj = ObjectHandle(self.store, self.name)

    # def testBadKey(self):
    #     self.store.get.return_value = 4
    #     self.obj.x

    def testSet(self):
        self.obj.x = 4
        self.store.set.assert_called_once_with(self.name, "x", 4)

    def testSetMulti(self):
        self.obj.x = 4
        self.store.set.assert_called_once_with(self.name, "x", 4)
        self.store.set.reset_mock()
        self.obj.y = 5
        self.store.set.assert_called_once_with(self.name, "y", 5)

    def testGet(self):
        self.obj.x = 4
        self.obj.y = 5
        self.store.get.return_value = {"x": 4}
        self.assertEqual(self.obj.x, 4)
        self.store.get.return_value = {"y": 5}
        self.assertEqual(self.obj.y, 5)


if __name__ == '__main__':
    unittest.main()
