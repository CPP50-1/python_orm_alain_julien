def char_field(func):
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    wrapper.field_type = "VARCHAR(255)"
    return wrapper
