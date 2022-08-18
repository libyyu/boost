# -*- coding: utf-8 -*-
# 
# 
import time
import logging

class UnknownDB(Exception):
    """raised for unsupported dbms"""
    pass

class InterfaceMethodException(Exception):
    """docstring for InterfaceMethodException"""
    def __init__(self, method):
        super(InterfaceMethodException, self).__init__()
        self.method = method
    def __str__(self):
        return "Can not call interface method {0}".format(self.method)

_databases = {}
def database(dbname=None):
    if dbname and _databases[dbname]:
        return _databases[dbname]()
    else:
        raise UnknownDB, dbname

def register_database(name, clazz):
    """
    Register a database.
        class LegacyDB(DB):
        ...     def __init__(self, **params): 
        ...        pass 
        ...
        register_database('legacy', LegacyDB)
        db = database(dbn='legacy', db='test', user='joe', passwd='secret')
    """
    _databases[name] = clazz

def import_driver(drivers, preferred=None):
    """Import the first available driver or preferred driver.
    """
    if preferred:
        drivers = [preferred]

    for d in drivers:
        try:
            return __import__(d, None, None, ['x'])
        except ImportError:
            pass
    raise ImportError("Unable to import " + " or ".join(drivers))

class DBAPI:
    """docstring for DBAPI"""
    def connect(self, **kw):
        raise InterfaceMethodException("DBAPI.connect")

    def close(self):
        raise InterfaceMethodException("DBAPI.close")

    def query(self, query, asyncall = None, *parameters, **kwparameters):
        raise InterfaceMethodException("DBAPI.query")

    def execute(self, sql, *parameters, **kwparameters):
        raise InterfaceMethodException("DBAPI.execute")

    def has_database(self, dbname):
        raise InterfaceMethodException("DBAPI.has_database")

    def use_database(self, dbname):
        raise InterfaceMethodException("DBAPI.use_database")

    def has_table(self, tbname):
        raise InterfaceMethodException("DBAPI.has_table")

    def autocommit(self, auto=True):
        raise InterfaceMethodException("DBAPI.autocommit")

    def commit(self):
        raise InterfaceMethodException("DBAPI.commit")

class DBMySQL(DBAPI):
    """docstring for DBMySQL"""
    def __init__(self):
        self._conn = None
        self.max_idle_time = 7 * 3600
    def __del__(self):
        self.close()
    def connect(self, **kw):
        self._db_args = dict(kw)
        self._last_use_time = time.time()
        self.__reconnect()
    def close(self):
        try:
            if self._conn is not None:
                self._conn.close()
                self._conn = None
                print "connection is closed."
        except Exception as e:
            raise e

    def __reconnect(self):
        try:
            import MySQLdb
            self._conn = MySQLdb.connect(**self._db_args)
            print "success connect to mysql."
        except Exception as e:
            raise e
        finally:
            pass
    def __ensure_connected(self):
        if (self._conn is None or
            (time.time() - self._last_use_time > self.max_idle_time)):
            self.__reconnect()
        self._last_use_time = time.time()
    def __cursor(self):
        self.__ensure_connected()
        return self._conn.cursor()
    def query(self, query, asyncall = None, *parameters, **kwparameters):
        cursor = self.__cursor()
        try:
            result = self.__execute(cursor, query, *parameters, **kwparameters)
            if asyncall is not None:
                asyncall(result, cursor)
            return len(cursor.fetchall())
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def execute(self, sql, *parameters, **kwparameters):
        cursor = self.__cursor()
        try:
            return self.__execute(cursor, sql, *parameters, **kwparameters)
        finally:
            cursor.close()

    def __execute(self, cursor, sql, *parameters, **kwparameters):
        try:
            result = cursor.execute(sql, kwparameters or parameters)
            return result
        except Exception as e:
            logging.error("Error execute for MySQL on %s", sql.format(kwparameters or parameters) if kwparameters or parameters else sql)
            raise e
        finally:
            pass

    def has_database(self, dbname):
        try:
            result = self.execute("SHOW DATABASES LIKE %s", dbname)
            return result == 1
        except Exception as e:
            raise e
            return False

    def use_database(self, dbname):
        try:
            self.execute("use " + dbname)
        except Exception as e:
            raise e

    def has_table(self, tbname):
        try:
            result = self.execute("SHOW TABLES LIKE %s", tbname)
            return result == 1
        except Exception as e:
            raise e
            return False

    def autocommit(self, auto=True):
        try:
            self._conn.autocommit(auto)
        except Exception as e:
            raise e

    def commit(self):
        try:
            self._conn.commit()
        except Exception as e:
            raise e
register_database('mysql', DBMySQL)

class DBSQLite(DBAPI):
    """docstring for DBSQLite"""
    def __init__(self):
        self._conn = None
        self.max_idle_time = 7 * 3600
    def __del__(self):
        self.close()
    def connect(self, **kw):
        self._db_args = dict(kw)
        self._last_use_time = time.time()
        self.__reconnect()
    def close(self):
        try:
            if self._conn is not None:
                self._conn.close()
                self._conn = None
                print "connection is closed."
        except Exception as e:
            raise e

    def __reconnect(self):
        try:
            sqlite = import_driver(["sqlite3", "pysqlite2.dbapi2", "sqlite"])
            self._conn = sqlite.connect(**self._db_args)
            print "success connect to sqlite."
        except Exception as e:
            raise e
        finally:
            pass
    def __ensure_connected(self):
        if (self._conn is None or
            (time.time() - self._last_use_time > self.max_idle_time)):
            self.__reconnect()
        self._last_use_time = time.time()
    def __cursor(self):
        self.__ensure_connected()
        return self._conn.cursor()
    def query(self, query, asyncall = None, *parameters, **kwparameters):
        cursor = self.__cursor()
        try:
            result = self.__execute(cursor, query, *parameters, **kwparameters)
            if asyncall is not None:
                asyncall(result, cursor)
            return len(cursor.fetchall())
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def execute(self, sql, *parameters, **kwparameters):
        cursor = self.__cursor()
        try:
            result = self.__execute(cursor, sql, *parameters, **kwparameters)
            return result.rowcount
        finally:
            cursor.close()

    def __execute(self, cursor, sql, *parameters, **kwparameters):
        try:
            result = cursor.execute(sql, kwparameters or parameters)
            return result
        except Exception as e:
            logging.error("Error execute for SQLite on %s", sql.format(kwparameters or parameters) if kwparameters or parameters else sql)
            raise e
        finally:
            pass

    def has_database(self, dbname):
        pass

    def use_database(self, dbname):
        pass

    def has_table(self, tbname):
        cursor = self.__cursor()
        try:
            self.__execute(cursor, "select count(*)  from sqlite_master where type='table' and name='%s'" % tbname)
            cnt = cursor.fetchone()[0]
            return int(cnt) == 1
        except Exception as e:
            raise e
            return False
        finally:
            cursor.close()

    def autocommit(self, auto=True):
        pass
    def commit(self):
        try:
            self._conn.commit()
        except Exception as e:
            raise e
register_database('sqlite', DBSQLite)


def test_mysql():
    o = database(dbname='mysql')
    print o.connect(host="localhost",user="root",passwd="199010", charset="utf8")
    print o.has_database("go886")
    o.use_database("go886")
    print o.has_table("tb_user")
    def showall(result, cursor):
        for v in cursor.fetchall():
            print v
        pass
    o.query("select * from tb_user", showall)

def test_sqlite():
    o = database(dbname='sqlite')
    print o.connect(database="go886")
    print o.has_database("go886")
    o.use_database("go886")
    o.execute('''CREATE TABLE IF NOT EXISTS `tb_user`
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
    #o.execute("INSERT INTO tb_user (ID,NAME,AGE,ADDRESS,SALARY) VALUES (6, 'Paul', 32, '北京 Beijing', 20000.00 )");
    #print o.execute("DELETE FROM tb_user WHERE NAME=?", ('Paul'))
    print o.has_table("tb_user")
    o.commit()
    def showall(result, cursor):
        for v in cursor.fetchall():
            print v
        pass
    o.query("select * from tb_user",showall)

def main():
    #test_mysql()
    test_sqlite()


if __name__ == '__main__':
    main()
