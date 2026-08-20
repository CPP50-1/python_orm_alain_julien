def boolean_field(func):
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    wrapper.field_type = "BOOLEAN"
    return wrapper
