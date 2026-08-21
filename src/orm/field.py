
class Field:
    def __init__(self, unique, foreign, default_value, required, expected_type):
        self.attribute_name = None
        self.sql_type = expected_type # supplied by the subclass
        self.unique = unique # todo needed?
        self.foreign = foreign # todo needed?
        self.default_value = default_value
        self.required = required # todo needed?

    def __set_name__(self, owner, name):
        self.attribute_name = name
        owner._fields[name] = self

    def __get__(self, instance, owner):
        if instance:
            return instance.__dict__[self.attribute_name]
        else:
            return self # Class-call, return the descriptor

    def __set__(self, instance, value):
        '''
        update the instance field to the supplied value.
        The instance is marked as dirty if there is a actual value change and the attribute is added
        to instance dirty_field set (So we know what columns to sql UPDATE).
        :param instance: the instance to which this field belongs
        :param value: the value to set
        :return: None
        :exception: ValueError: unsupported value
        '''
        try:
            value = self.check_and_coerce(value)
        except ValueError as e:
            raise e
        value_change = False
        try:
            current_value = instance.__dict__[self.attribute_name]
            value_change = current_value != value
        except KeyError as e:
            # No value yet. Won't mark as dirty
            instance.__dict__[self.attribute_name] = value

        if value_change:
            instance.__dict__[self.attribute_name] = value
            instance._is_dirty = True
            instance._dirty_fields.add(self.attribute_name)

    def check_and_coerce(self, value):
        '''
        Default method. No check
        :param value:
        :return: the supplied value or the default if the value is None
        '''
        return value or self.default_value

class BooleanField(Field):
    def __init__(self, unique:bool=False, foreign:bool=False, required:bool=True, default_value=None):
        super().__init__(unique, foreign, default_value, required, "BOOLEAN")

    def check_and_coerce(self, value) -> bool:
        '''
        Verify value is an int or a stringified int
        :param value: the value to be checked
        :return: the value coerced to a bool
        :exception ValueError: never raised
        '''
        if value is None:
            return self.default_value
        return True if value else False

class IntegerField(Field):
    def __init__(self, unique:bool=False, foreign:bool=False, default_value=None, required=True):
        super().__init__(unique, foreign, default_value, required, "INT")

    def check_and_coerce(self, value) -> int:
        '''
        Verify value is an int or a stringified int
        :param value: the value to be checked
        :return: the value coerced to an int
        :exception ValueError: if value may not be coerced to an int
        '''
        if value is None:
            return self.default_value
        if isinstance(value, int):
            return value
        return int(value) # may raise ValueError

class SerialField(Field):
    def __init__(self, unique:bool=True, foreign:bool=False, default_value=None, required=False):
        super().__init__(unique, foreign, default_value, required, "SERIAL")

    def check_and_coerce(self, value) -> int|None:
        '''
        Verify value is an (possibly stringified) int or None. However, if None, don't use the default
        :param value: the value to be checked
        :return: the value coerced to an int
        :exception ValueError: if value may not be coerced to an int
        '''
        if isinstance(value, int):
            return value
        elif value is None:
            return None
        else:
            return int(value) # may raise ValueError

class CharField(Field):
    def __init__(self, unique: bool = False, foreign: bool = False, default_value=None, required:bool=True, max_len=None):
        super().__init__(unique, foreign, default_value, required, f"VARCHAR({max_len})" if max_len else "TEXT")
        self.max_len = max_len

    def check_and_coerce(self, value) -> str:
        '''
        Verify the stringified version of the value isn't too long
        :param value: the value to be checked
        :return: the value coerced to a string
        :exception ValueError: if the coerced value is longer than max_len
        '''
        if value is None:
            return self.default_value
        str_value = str(value)
        if self.max_len and len(str_value) > self.max_len:
            raise ValueError(f'Too long value \\{value}\\ for {self.attribute_name}. Max length is {self.max_len}')
        return str_value

if __name__=="__main__":
    def test(bool_value, int_value, char_value):
        try:
            instance = TestTable(bool_value, int_value, char_value)
            print(instance)
            return instance
        except ValueError as e:
            print(f"{bool_value}, {int_value}, {char_value} => {e}")
            return None

    class TestTable():
        bool_column = BooleanField(default_value=True)
        int_column = IntegerField(default_value=999)
        char_column = CharField(max_len=10, default_value="-", required=False)

        def __init__(self, bool_value, int_value, char_value):
            self.bool_column = bool_value
            self.int_column = int_value
            self.char_column = char_value

        def __str__(self):
            return f"TestTable({self.bool_column}, {self.int_column}, {self.char_column})"

    i4 = test(False, 122.9, "A 2long str")
    i1 = test(True, 123, "ABC")
    i2 = test(False, "234", "ABCDEFGHIJ")
    i3 = test(False, "234s", "ABCDEFGHIJ")
    i5 = test(False, None, char_value=None)

