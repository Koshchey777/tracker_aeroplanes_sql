import psycopg2

def create_database(namedb):
    conn = psycopg2.connect(database=namedb)
