from psycopg2 import OperationalError
import psycopg2


def create_connection(db_first_name, db_user, db_password, db_host):
    connection = None

    try:
        connection = psycopg2.connect(
            database=db_first_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        print("connection to Postgresql")
    except OperationalError as e:
        print(f"The error {e} occurred")
    return connection


connection = create_connection(
    "postgres", "postgres", "abc123", "127.0.0.1")


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor

    try:
        cursor.exexute(query)
        print("Query execute successfully")
    except OperationalError as e:
        print(f"The error {e} occurred")


create_database_query = "CREATE DATABASE sm_ap"
create_database(connection, create_database_query)
