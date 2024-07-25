def validate_params(func):
    def wrapper(*args, **kwargs):
        for param in args:
            if param is None or (isinstance(param, (str, list, dict, set)) and not param):
                print("Error: One or more parameters are None or empty.")
                return None
        return func(*args, **kwargs)
    return wrapper