import psycopg2


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

def create_db(dbConnConfig):
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = "CREATE TABLE IF NOT EXISTS docType (type_id INT NOT NULL, type_name varchar(250) NOT NULL, PRIMARY KEY (type_id));" 
        cursor.execute(sqlStatement,(CREATE_FLG,))
        connection.commit()
        
        sqlStatement = "CREATE TABLE IF NOT EXISTS db1 (doc_id INT NOT NULL, title varchar(250) NOT NULL, type_id INT NOT NULL REFERENCES docType (type_id), PRIMARY KEY (doc_id));" 
        cursor.execute(sqlStatement,(CREATE_FLG,))
        connection.commit()

        sqlStatement = "CREATE TABLE IF NOT EXISTS db2 (doc_id INT NOT NULL, title varchar(250) NOT NULL, type_id INT NOT NULL REFERENCES docType (type_id), PRIMARY KEY (doc_id));" 
        cursor.execute(sqlStatement,(CREATE_FLG,))
        connection.commit()

        sqlStatement = "CREATE TABLE IF NOT EXISTS db3 (doc_id INT NOT NULL, title varchar(250) NOT NULL, type_id INT NOT NULL REFERENCES docType (type_id), PRIMARY KEY (doc_id));" 
        cursor.execute(sqlStatement,(CREATE_FLG,))
        connection.commit()

        sqlStatement = "CREATE TABLE IF NOT EXISTS db4 (doc_id INT NOT NULL, title varchar(250) NOT NULL, type_id INT NOT NULL REFERENCES docType (type_id), PRIMARY KEY (doc_id));" 
        cursor.execute(sqlStatement,(CREATE_FLG,))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed create ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def insertData(dbConnConfig):
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        type_data = [
            (1, 'tesis'),
            (2, 'libro'),
            (3, 'video'),
            (4, 'presentacion')
        ]

        sqlStatement = "INSERT INTO docType (type_id, type_name) VALUES (%s, %s) ON CONFLICT (type_id) DO NOTHING;"
        cursor.executemany(sqlStatement, type_data)
        connection.commit()

        for i in range(1,10):
            #db1
            sqlStatement = f"INSERT INTO db1 (doc_id, title, type_id) VALUES ({i}, 'tesis {i}', {1}) ON CONFLICT (doc_id) DO NOTHING;"
            cursor.execute(sqlStatement,(CREATE_FLG,))
            connection.commit()
            #db2
            sqlStatement = f"INSERT INTO db2 (doc_id, title, type_id) VALUES ({i}, 'libro {i}', {2}) ON CONFLICT (doc_id) DO NOTHING;"
            cursor.execute(sqlStatement,(CREATE_FLG,))
            connection.commit()
            #db3
            sqlStatement = f"INSERT INTO db3 (doc_id, title, type_id) VALUES ({i}, 'video {i}', {3}) ON CONFLICT (doc_id) DO NOTHING;"
            cursor.execute(sqlStatement,(CREATE_FLG,))
            connection.commit()
            #db4
            sqlStatement = f"INSERT INTO db4 (doc_id, title, type_id) VALUES ({i}, 'presentacion {i}', {4}) ON CONFLICT (doc_id) DO NOTHING;"
            cursor.execute(sqlStatement,(CREATE_FLG,))
            connection.commit()

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed select ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def select_all(dbConnConfig, table):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = f"SELECT * FROM {table};"
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

def select_byFilter(dbConnConfig,table, title):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()
        print ("list products by args => title={}".format(title))
        sqlStatement=""
        if title != None:
            print(1)
            sqlStatement = f"select * from {table} where title=%s"
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