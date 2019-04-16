import uuid
import datetime
import numpy as np

class DEBasic:
    def __init__(self, tablealias = "b01", colname = None, proptype = str, dbtype=None, isprimary=False):
        self.tablealias = tablealias
        self.colname = colname if colname != None else proptype
        self.proptype = proptype
        self.dbtype = dbtype
        self.isprimary = isprimary

class DEDateTime(DEBasic):
    def __init__(self, tablealias = "b01", colname = None):
        super().__init__(tablealias=tablealias, colname=colname, proptype=datetime, dbtype="TIMESTAMP")

class DEGid(DEBasic):
    def __init__(self, tablealias = "b01", colname = None):
        super().__init__(tablealias=tablealias, colname=colname, proptype=str, dbtype="uuid", isprimary=True)

class DEForeignKey(DEBasic):
    def __init__(self, tablealias = "b01", colname = None):
        super().__init__(tablealias=tablealias, colname=colname, proptype=str, dbtype="uuid")

class DEText(DEBasic):
    def __init__(self, tablealias = "b01", colname = None):
        super().__init__(tablealias=tablealias, colname=colname, proptype=str, dbtype="TEXT")

class DENumpyArray(DEBasic):
    def __init__(self, tablealias = "b01", colname = None):
        super().__init__(tablealias=tablealias, colname=colname, proptype=np.array, dbtype="nparray")

JOINTYPEINNER = "left inner"
JOINTYPEOUTER = "outer"

class DTTableEntry:
    def __init__(self, name=None, joindef=None, jointype=None):
        """contructor for a new table entry
           name: full name of table
           joindef: definition of the join like a where clause
           jointype: type of join, use constants like JOINTYPEINNER, JOINTYPEOUTER
        """
        self.name = name #the table's name
        self.joindef = joindef #a join definition like: left inner join other_table other on b01.x=other.y
        self.jointype = jointype



class DTBasic:
    """basic object from which all other data objects are derived
    """
    persistents = {
            "gid": DEGid(colname="gid"), 
            "created":DEDateTime(colname="created"),
            "updated":DEDateTime(colname="updated")
    }

    tables = {"b01" : DTTableEntry()}

    def __init__(self):
        self.ispersist = False
        self.gid = uuid.uuid4()
        self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()