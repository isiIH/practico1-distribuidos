import psycopg2
from common import sysConfig


###############################################################################
def get_connection_db(conn):
    return psycopg2.connect(user=conn["user"],
                            password=conn["pass"],
                            host=conn["host"],
                            port=conn["port"],
                            database=conn["dbname"])

###############################################################################

CREATE_FLG="0"
DELETE_FLG="-1"

def select_all(dbConnConfig):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = f"SELECT * FROM {sysConfig['db_name']};"
        cursor.execute(sqlStatement)
        resp = cursor.fetchall()

    except (Exception, psycopg2.Error) as error :
        resp=str(error)
        if(connection):
            print("Failed select ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return resp

def select_byFilter(dbConnConfig, title):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()
        print ("list products by args => title={}".format(title))
        sqlStatement=""
        if title != None:
            print(1)
            sqlStatement = f"select * from {sysConfig['db_name']} where title=%s"
            cursor.execute(sqlStatement,(title,))
        resp = cursor.fetchall()

    except (Exception, psycopg2.Error) as error :
        resp=str(error)
        if(connection):
            print("Failed select ", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return resp