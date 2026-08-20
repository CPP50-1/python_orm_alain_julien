import psycopg2


class Database:
    @staticmethod
    def connect(host: str, database: str, user: str, password: str):
        """Connect to the PostgreSQL database server"""
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(
                host=host, database=database, user=user, password=password
            ) as conn:
                print("Connected to the PostgreSQL server.")
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
