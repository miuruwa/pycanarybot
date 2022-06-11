import sqlite3




def init():
    global __connection, conn, c
    __connection = None
    conn = get_connection('database.db')
    c = conn.cursor()
def get_connection(baseName: str):
    __connection = sqlite3.connect(baseName)
    return __connection
    

def find(selectstr: str, fromstr: str):
    c.execute("SELECT {} FROM {}".format(selectstr, fromstr))
    return c.fetchall()

def findw(selectstr: str, fromstr: str, where: str):
    c.execute("SELECT {} FROM {} WHERE {}".format(selectstr, fromstr, where))
    return c.fetchall()
    
def update(updatestr: str, setstr: str, where: str):
    c.execute("UPDATE {} SET {} WHERE {}".format(updatestr, setstr, where))
    conn.commit()
    
def insert(insertstr: str, intostr: str):
    #c.execute(" SELECT {} WHERE NOT EXISTS(SELECT 1 FROM {} WHERE {}".format(intostr, insertstr, intostr, where))
    c.execute("INSERT INTO {} VALUES({})".format(intostr, insertstr))
    conn.commit()