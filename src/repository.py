import os

from database import Database
from src.base_entity import BaseEntity


class Repository:

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        entities,
    ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.entities: list[BaseEntity] = entities

    def create_migration(self, name: str):
        filename = f"migrations/{name.replace(" ", "_")}.sql"
        content = ""
        for entity in self.entities:
            content += entity().generate_sql()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a") as f:
            f.write(content)

    def run_migrations(self):
        connection = Database.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        with connection.cursor() as cursor:
            with open("migrations/add_myclass_table.sql", "r") as file:
                query = file.read().replace("\n", "")
                cursor.execute(query=query)
                connection.commit()
