import uuid
import datetime
from DataBasic import DTBasic, DEDateTime, DEForeignKey, DEText, DENumpyArray
from DataGroup import DataGroup

class DataCollection(DTBasic):
    """basic implementation of a class to store spectra data in da local database
    """
    SPECTRUM = "SP"
    MAP = "MA"
    persistents = DTBasic.persistents.copy()
    persistents.update({"name": DEText(colname="name"),
                     "coll_type": DEText(colname="coll_type"),
                     "parent_id": DEForeignKey(colname="parent_id"),
                     "group_id": DEForeignKey(colname="group_id"),
                     "data": DENumpyArray(colname="data")})

    def __init__(self):
        self.gid = str(uuid.uuid4())
        self.ispersist = False
        self.coll_type = DataCollection.SPECTRUM
        self.created = datetime.datetime.now()
        self.updated = self.created
        self.name = "Spectra " + str(self.created)
        self.parent_id = None
        self.group_id = None
        self.data = None


    def set_data(self, data):
        self.data = data
