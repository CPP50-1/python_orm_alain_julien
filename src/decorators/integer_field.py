def integer_field(func):
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    wrapper.field_type = "INTEGER"
    return wrapper
