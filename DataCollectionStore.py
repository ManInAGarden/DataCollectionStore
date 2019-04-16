import sqlite3
import datetime
import uuid
import numpy as np
import io

from DataCollection import *


class DataCollectionStore:
    """Class representing a complete data base for spdatacollections.
       This is a factory for all data objects needed for that
    """
    registered = False

    def __init__(self, name, dbfilename):
        self.name = name
        self.dbfilename = dbfilename
        self.__in_transaction = None

        if not DataCollectionStore.registered:
            sqlite3.register_adapter(np.ndarray, DataCollectionStore.adapt_array)
            sqlite3.register_converter("nparray", DataCollectionStore.convert_array)
            sqlite3.register_adapter(uuid.UUID, DataCollectionStore.adapt_uuid)
            sqlite3.register_converter("uuid", DataCollectionStore.convert_uuid)
        self.conn = sqlite3.connect(dbfilename, detect_types=sqlite3.PARSE_DECLTYPES)

    def dispose_me(self):
        """dispose the store after any work has been done
        """
        self.conn.close()

    def create_tables(self):
        """method for creation of all data base tables needed
        """
        self.conn.execute("create table coll (gid uuid PRIMARY KEY NOT NULL, name TEXT NOT NULL, parent_id uuid, group_id uuid NOT NULL, spec_type TEXT, data nparray, created TIMESTAMP, updated TIMESTAMP)")
        self.conn.execute("create table coll_grp (gid uuid PRIMARY KEY NOT NULL, name TEXT NOT NULL, grp_type TEXT, created TIMESTAMP, updated TIMESTAMP)")


    def alter_tables(self, fromversion, toversion):
        """update table definition when upgrading from on version of the database
           to a new version
        """
        pass

    def begin_transaction(self):
        self.__in_transaction = True

    def rollback_transaction(self):
        if not self.__in_transaction:
            raise Exception("Rollback with no running transaction")
        else:
            conn.Rollback()
            self.__in_transaction = False

    def commit_transaction(self):
        if not self.__in_transaction:
            raise Exception("Rollback with no running transaction")
        else:
            conn.commit()
            self.__in_transaction = False

    def flush(self, dob):
        """store the data object to the database
           dob: instance of data object to be flushed
           returns: instance of flushed object with any changes during flush
        """
        if not issubclass(type(dob), DTBasic):
            raise Exception("only subclasses of DTBasic can be flushed.")

        if dob.ispersist:
            self.__do_update(dob)
        else:
            self.__do_insert(dob)

        if self.__in_transaction == None:
            self.conn.commit()

        return dob

    def __do_insert(self, dob):
        dob_class = type(dob)
        pers = dob_class.persistents
        tabs = dob_class.tables
        cols, marks = self.__getcolsforins(pers)
        stmt = "insert into {} ({}) values({})".format(tabs["b01"].name,
            cols, 
            marks)
        dattup = self.__getproptuple(dob, pers, "b01")
        self.conn.execute(stmt, dattup)
        dob.ispersist = True

    def __getproptuple(self, dob, pers, tablealias):
        """get the proptuple for a table
        """
        answ = []
        
        for key, pentry in pers.items():
            if pentry.tablealias == tablealias:
                answ.append(getattr(dob, key, "None"))

        return tuple(answ)

    def __getcolsforins(self, ps):
        cols = None
        marks = None
        first = True
        for key in ps:
            pentry = ps[key]
            if pentry.tablealias == "b01":
                if first:
                    cols = pentry.colname 
                    marks = "?"
                    first = False
                else:
                    cols += ", " + pentry.colname
                    marks += ",?"

        return cols, marks


    def __do_update(self, dob):
        dob_class = type(dob)
        pers = dob_class.persistents
        tabs = dob_class.tables
        sets = self.__getupsforup(pers)
        wc = "b01.gid=?"
        stmt = "update {} {} set {} where {})".format(tabs["b01"].name,
            "b01",
            sets, 
            wc)
        dattup = self.__getproptuple(dob, pers, "b01")
        self.conn.execute(stmt, dattup + (getattr(dob, "gid", "None"),))

    def __getupsforup(self, pers):
        answ = None
        first = True
        for key, perentry in pers.items():
            if perentry.tablealias == "b01" and key != "gid":
                if first:
                    answ = "{}=?".format(perentry.colname)
                    first = False
                else:
                    answ += ", {}=?".format(perentry.colname)
        return answ

    def getbygid(self, t, gid):
        dob = t()
        selcols = self.__get_sel_cols(t)
        seltables = self.__get_sel_tables(t)
        stmt = "select {} from {} where gid=:gid".format(selcols, seltables)
        curs = self.conn.cursor()
        res = curs.execute(stmt, {"gid": gid})
        row = res.fetchone()

        for key, pentry in t.persistents:
            setattr(dob.key, self.__get_val_obj_style(pentry, row[key]))

        return dob

    def __get_val_obj_style(self, pentry, value):
        if value == None:
            return None

        valt = type(value)
        if pentry.proptype == valt:
            return value

        raise NotImplementedError("unknown type combination in property <{}> and database's select result <{}>".format(pentry.proptype,
            valt))

        return str(value)

    def __get_sel_cols(self, t):
        """get the columns to be used in data selects
        """
        answ = None
        for pname, pentry in t.persistents.items():
            if answ == None:
                answ = "{}.{} as {}".format(pentry.tablealias, pentry.colname, pname)
            else:
                answ += ", {}.{} as {}".format(pentry.tablealias, pentry.colname, pname)

        return answ

    def __get_sel_tables(self, t):
        answ = None
        for tabalias, tentry in t.tables.items():
            if answ == None:
                answ = self.__get_single_sel_table(tabalias, tentry)
            else:
                answ += ", " + self.__get_single_sel_table(tabalias, tentry)
        return answ

    def __get_single_sel_table(self, tabalias, tentry):
        if tentry.joindef == None:
            return tentry.name + " " + tabalias
        else:
            return "{} join {} {} on {}".format(tentry.jointype, 
                tentry.name, 
                tabalias,
                tentry.joindef)

    def delete(self, do):
        pass
        
    @classmethod
    def adapt_array(cls, arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    @classmethod
    def convert_array(cls, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    @classmethod
    def adapt_uuid(cls, gid):
        return str(gid)

    @classmethod
    def convert_uuid(cls, text):
        return uuid.UUID(hex=text)


