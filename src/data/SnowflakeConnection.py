import snowflake.connector
import logging
from decouple import config

DEBUG = config('DEBUG', cast=bool)

DATABASES = {
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'ACCOUNT': config('DB_ACCOUNT'),
        'DATABASE': config('DB_NAME'),
        'SCHEMA': config('DB_SCHEMA'),
        'WAREHOUSE': config('DB_WAREHOUSE'),
    }


def connectionBD():
    """
    Connection to DB with snowflake
    """

    USER = DATABASES["USER"]
    PASSWORD = DATABASES["PASSWORD"]
    ACCOUNT = DATABASES["ACCOUNT"]
    DATABASE = DATABASES["DATABASE"]
    SCHEMA = DATABASES['SCHEMA']
    WAREHOUSE = DATABASES["WAREHOUSE"]

    try:
        conn = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
            database=DATABASE,
            schema=SCHEMA,
            warehouse=WAREHOUSE,
        )
        logging.info("connection success")
        # assert  None
        return conn
    except Exception as e:
        logging.warning(f'Connection failed: {str(e)}')
        return None


if __name__ == '__main__':
    conn = connectionBD()
    print("RETURN")
    print(type(conn))
    print(conn)

    if conn != None:
        print("YES")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Compra" LIMIT 10')

        for row in cursor.fetchall():
            print(row)  

        cursor.close()
        conn.close()
