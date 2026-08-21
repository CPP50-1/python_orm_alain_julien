from abc import ABC, ABCMeta

from src.orm.field import CharField, BooleanField, IntegerField, SerialField, Field

TABLE_NAME_ATTR = "_table_name" # The class attribute name to use in BaseEntity subclasses for specifying the mapped SQL table name

verbose = True

class ModelMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        if verbose: print(f"Creating model class {name}")
        # Add two class attributes:
        #   id as a SerialField
        #   _fields to hold the mapping from attribute name to field, populated through the Field __set_name__ method
        attrs.update({'_fields': {}, 'id':SerialField()})
        # create the class
        cls = super().__new__(mcs, name, bases, attrs)
        if table_name:=attrs.get(TABLE_NAME_ATTR):
            # Use the TABLE_NAME_ATTR specified on the class to create or else the class name in lowercase
            bases[0]._model_registry[cls] = table_name or name.lower() # todo convert camel case name to snake case name

            if verbose: print(f"Registering model class {name} with attributes {cls._fields.items()}")

        return cls

class BaseEntity(ABC, metaclass=ModelMeta):
    # The registry of models/entities derived from BaseEntity as a mapping from Class to SQL table name
    _model_registry : dict["BaseEntity", str] = {}

    def __init__(self):
        self.id = None
    def __init__(self):
        self.id = None
        self._is_dirty = False # todo is it ok on creation?
        self._dirty_fields = set()
        self._in_db = False

    @classmethod
    def generate_sql(self):
        columns = []

        for name, attr in self._fields.items():
            if isinstance(attr, SerialField):
                # Place the serial as 1st column
                columns.insert(0, f"{name} {attr.sql_type}")
            elif isinstance(attr, Field):
                # Columns order =  field declaration order
                columns.append(f"{name} {attr.sql_type}")
            #if callable(attr) and hasattr(attr, "field_type"):
            #    columns.append(f"{name} {attr.field_type}")

        sql = f"CREATE TABLE {self._table_name} (\n"
        sql += ",\n".join(columns)
        sql += "\n);\n"

        return sql

if __name__ == "__main__":
    # Example usage
    class Customer(BaseEntity):
        _table_name = "customer"

        name = CharField(max_len=40)
        city = CharField(max_len=40)
        vip = BooleanField()

        def __init__(self, name:str, city:str, vip: bool):
            super().__init__()
            self.name = name
            self.city = city
            self.vip = vip

    class Order(BaseEntity):
        _table_name = "order"
        reference = CharField(max_len=40)
        amount = IntegerField()
        customer = IntegerField()

        def __init__(self, name:str, amount:int, customer:int):
            super().__init__()
            self.id = None
            self.name = name
            self.amount = amount
            self.customer = customer

    donald = Customer("Donald","Mar a Lago", vip=False)
    print(f"Customer {donald.name} is{'' if donald.vip else ' not'} a vip")

    order = Order("pound of mediocrity", 99, donald.id)
    print(f"Customer {order.customer} ordered {order.amount} {order.name}")

    print(f"Model : {BaseEntity._model_registry}")
    print(f"{donald._is_dirty}")

    order.amount += 0
    print(f"{order._is_dirty}")

    order.amount += 100
    print(f"{order._is_dirty}")

    print(Customer.generate_sql())
    print(Order.generate_sql())