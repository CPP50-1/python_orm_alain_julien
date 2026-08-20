import os

from src.base_entity import BaseEntity


class Repository:

    def __init__(self, entities):
        self.entities: list[BaseEntity] = entities

    def create_migration(self, name: str):
        filename = f"migrations/{name.replace(" ", "_")}.sql"
        content = ""
        for entity in self.entities:
            content += entity().generate_sql()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a") as f:
            f.write(content)
