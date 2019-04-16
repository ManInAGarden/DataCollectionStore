import datetime
import uuid

class DataGroup:
    """class to persist data groups which are containers
       for data collections
    """

    def __init__(self):
        self.ispersist = False
        self.name = "New Collection"
        self.created = datetime.datetime.now()
        self.updated = self.created
        self.gid = uuid.uuid4()
        self.collections = None

    def fetch_all_collections(self):
        """ fetch all collections which are associated with this group
        """
        pass

    def fetch_collections(self, coltypes):
        """fetch the collections associated with this group
           which are of one of the given collection-types
        """
        pass