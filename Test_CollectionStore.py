import unittest
import os
import os.path
import time
import numpy as np

from DataBasic import DTBasic
from CollectionGroup import CollectionGroup
from DataCollectionStore import DataCollectionStore
from DataCollection import *

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
        oldupdated = grp.updated
        grp.name = "name changed"
        self.stflush(grp) #update
        time.sleep(1)
        self.assertGreater(grp.updated, oldupdated)
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
        self.assertEqual(grp.updated, grpr.updated)
        self.assertEqual(grp.grp_type, grpr.grp_type)

    def test_040group_delete(self):
        grp = CollectionGroup()
        grp.name = "a group to be deleted UT"
        self.stflush(grp)
        grpr = self.stgetbygid(CollectionGroup, grp.gid)
        self.assertIsNotNone(grpr)
        self.sstore.delete(grp)
        grpr = self.stgetbygid(CollectionGroup, grp.gid)
        self.assertIsNone(grpr)

    def test_100coll_alldbops(self):
        defgrp = CollectionGroup()
        defgrp.name = "DEFAULT-GRP-UT#1"
        self.stflush(defgrp)

        coll = DataCollection()
        coll.name = "collection #1-UT"
        coll.group_gid = coll.gid
        self.stflush(coll)
        collr = self.stgetbygid(DataCollection, coll.gid)
        self.assertEqual(coll.gid, collr.gid)
        self.assertEqual(coll.name, collr.name)
        self.assertEqual(coll.grp_type, collr.grp_type)
    

    def stflush(self, dob):
        self.__class__.sstore.flush(dob)

    def stgetbygid(self, t, gid):
        return self.__class__.sstore.getbygid(t, gid)

if __name__ == '__main__':
    unittest.main()