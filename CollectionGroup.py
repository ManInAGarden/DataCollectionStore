from DataBasic import DTBasic, DTTableEntry, DEText

class CollectionGroup(DTBasic):

    NONETYPE="NT"
    
    tables = DTBasic.tables.copy()
    tables["b01"] = DTTableEntry(name="coll_grp")
    persistents = DTBasic.persistents.copy()
    persistents.update({"name": DEText(colname="name"),
                     "grp_type": DEText(colname="grp_type")})

    def __init__(self):
        super().__init__()
        self.name = "new collection group"
        self.grp_type = CollectionGroup.NONETYPE