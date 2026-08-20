from abc import ABC, abstractmethod


class BaseEntity(ABC):

    @abstractmethod
    def table_name(self):
        pass

    def generate_sql(self):
        columns = []

        for name, attr in self.__class__.__dict__.items():
            if callable(attr) and hasattr(attr, "field_type"):
                columns.append(f"{name} {attr.field_type}")

        sql = f"CREATE TABLE {self.table_name()} (\n"
        sql += ",\n".join(columns)
        sql += "\n);\n"

        return sql
