import os
import psycopg2

POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')

psyco = None
cursor = None

try:
    psyco = psycopg2.connect(
        host=POSTGRES_HOSTNAME,
        user=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DBNAME
    )

    cursor = psyco.cursor()

    cursor.execute("SELECT * FROM users")

    for row in cursor.fetchall():
        print(row)

    # psyco.commit()
    cursor.close()
    psyco.close()

except Exception as e:
    print(e)
finally:
    print("Done")
