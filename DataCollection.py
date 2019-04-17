import uuid
import datetime
from DataBasic import DTBasic, DEDateTime, DEForeignKey, DEText, DENumpyArray, DTTableEntry

class DataCollection(DTBasic):
    """basic implementation of a class to store spectra data in da local database
    """
    SPECTRUM = "SP"
    MAP = "MA"
    UNSPECIFIED = "./."

    tables = DTBasic.tables.copy()
    tables["b01"] = DTTableEntry(name="coll")

    persistents = DTBasic.persistents.copy()
    persistents.update({"name": DEText(colname="name"),
                     "coll_type": DEText(colname="coll_type"),
                     "parent_gid": DEForeignKey(colname="parent_gid"),
                     "group_gid": DEForeignKey(colname="group_gid"),
                     "data": DENumpyArray(colname="data")})

    def __init__(self):
        super().__init__()
        self.coll_type = DataCollection.UNSPECIFIED
        self.name = "Collection " + str(self.created)
        self.parent_id = None
        self.group_id = None
        self.data = None
