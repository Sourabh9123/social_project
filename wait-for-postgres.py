import sys
import psycopg2
from time import sleep
from psycopg2 import OperationalError

def wait_for_postgres(host, port, user, password, dbname, retries=30, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname
            )
            conn.close()
            print("PostgreSQL is ready!")
            return True
        except OperationalError as e:
            print(f"Attempt {attempt+1}: PostgreSQL not yet ready - {e}")
            attempt += 1
            sleep(delay)
    
    print("Timeout waiting for PostgreSQL.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python wait-for-postgres.py <host> <port> <user> <password> <dbname>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    dbname = sys.argv[5]

    wait_for_postgres(host, port, user, password, dbname)
