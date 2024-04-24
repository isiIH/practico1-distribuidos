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

def select_all(dbConnConfig):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = "select * from products where current_status=%s" 
        cursor.execute(sqlStatement,(CREATE_FLG,))
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

def select_byFilter(dbConnConfig,pname,price):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()
        print ("list products by args => pname={} - price={}".format(pname,price))
        sqlStatement=""
        if pname != None and price != None:
            print(1)
            sqlStatement = "select * from products where current_status=%s and pname=%s and price=%s"
            cursor.execute(sqlStatement,(CREATE_FLG,pname,price))
        else:    
            print(2)
            if pname != None:
                print(3)
                sqlStatement = "select * from products where current_status=%s and pname=%s"
                cursor.execute(sqlStatement,(CREATE_FLG,pname,))
            if price != None:
                print(4)
                sqlStatement = "select * from products where  current_status=%s and price=%s"
                cursor.execute(sqlStatement,(CREATE_FLG,price,))
        
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

def select_byId(dbConnConfig,id):
    resp=[]
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = "select * from products where current_status=%s and id=%s" 
        cursor.execute(sqlStatement, (CREATE_FLG,id,))
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


def insert(dbConnConfig,server_name, subscriber_name, data):
    resp={"inserted_rows":-1}
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = """INSERT INTO public.products 
        (pname, price, current_status, server_name, subscriber_name)
        VALUES (%s, %s, %s, %s, %s)"""

        cursor.execute(sqlStatement, (data["pname"],data["price"],CREATE_FLG,server_name, subscriber_name,))
        connection.commit()
        resp["inserted_rows"] = cursor.rowcount

    except (Exception, psycopg2.Error) as error :
        resp=str(error)
        if(connection):
            print("Failed insert one ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")        
    return resp

def update(dbConnConfig,id,data):
    resp={"updated_rows":-1}
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = """update public.products set pname=%s, price=%s,last_update_date=CURRENT_TIMESTAMP
                      where id=%s"""

        cursor.execute(sqlStatement, (data["pname"],data["price"],id,))
        connection.commit()
        resp["updated_rows"] = cursor.rowcount

    except (Exception, psycopg2.Error) as error :
        resp=str(error)
        if(connection):
            print("Failed update ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")        
    return resp

def delete_all(dbConnConfig):
    resp={"deleted_rows":-1}
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = """update public.products set current_status=%s,last_update_date=CURRENT_TIMESTAMP 
                    where current_status=%s"""

        cursor.execute(sqlStatement,(DELETE_FLG,CREATE_FLG,))
        connection.commit()
        resp["deleted_rows"] = cursor.rowcount

    except (Exception, psycopg2.Error) as error :
        resp=str(error)
        if(connection):
            print("Failed 'delete' (update) ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return resp

def delete_byId(dbConnConfig,id):
    resp={"deleted_rows":-1}
    try:
        connection = get_connection_db(dbConnConfig)
        cursor = connection.cursor()

        sqlStatement = """update public.products set current_status=%s,last_update_date=CURRENT_TIMESTAMP 
                    where current_status=%s and id=%s"""

        cursor.execute(sqlStatement,(DELETE_FLG,CREATE_FLG,id,))
        connection.commit()
        resp["deleted_rows"] = cursor.rowcount

    except (Exception, psycopg2.Error) as error :
        resp=str(error)
        if(connection):
            print("Failed 'delete' (update) ", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return resp
