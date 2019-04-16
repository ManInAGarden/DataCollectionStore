import unittest
import os
import os.path
import numpy as np

from DataBasic import DTBasic
from CollectionGroup import CollectionGroup
from DataCollectionStore import DataCollectionStore
from DataCollection import *
from DataGroup import *

class TestCollectionStore(unittest.TestCase):
    sstore = None
    dbfile = os.getcwd() + os.sep + "myutstore_basic.db"

    @classmethod
    def setUpClass(cls):
        cls.remove_files() #remove evtually left over files from previous tests
        cls.sstore = DataCollectionStore("MyTestStore", cls.dbfile)
        cls.sstore.create_tables()

    @classmethod
    def tearDownClass(cls):
        cls.sstore.dispose_me()
        cls.remove_files()

    @classmethod
    def remove_files(cls):
        if os.path.isfile(cls.dbfile): os.remove(cls.dbfile)
        journalf = cls.dbfile + "-journal"
        if os.path.isfile(journalf): os.remove(journalf)

    def test_000basic_creation(self):
        bdo = DTBasic()
        self.assertIsNotNone(bdo.gid)
        self.assertIsNotNone(bdo.created)
        self.assertIsNotNone(bdo.updated)
        self.assertFalse(bdo.ispersist)

    def test_010group_creation(self):
        grp = CollectionGroup()
        self.assertIsNotNone(grp.gid)
        self.assertIsNotNone(grp.updated)
        self.assertIsNotNone(grp.created)
        self.assertIsNotNone(grp.name)
        self.assertFalse(grp.ispersist)

    
    def test_020group_storage(self):
        grp = CollectionGroup()
        self.stflush(grp) #insert
        grp.name = "name changed"
        self.stflush(grp) #update
        grp2 = CollectionGroup()
        grp.name = "other name"
        self.stflush(grp2) #another insert

    def test_030group_storagenreading(self):
        grp = CollectionGroup()
        grp.name = "another group UT"
        self.stflush(grp)
        grpr = self.stgetbygid(CollectionGroup, grp.gid)
        self.assertEqual(grp.gid, grpr.gid)
        self.assertEqual(grp.name, grpr.name)
        self.assertEqual(grp.created, grpr.created)
        self.assertEqual(grp.grp_type, grpr.grp_type)

    def stflush(self, dob):
        self.__class__.sstore.flush(dob)

    def stgetbygid(self, t, gid):
        return self.__class__.sstore.getbygid(t, gid)

if __name__ == '__main__':
    unittest.main()