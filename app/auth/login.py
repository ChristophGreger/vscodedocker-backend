from flask import session


def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return "Not logged in", 401
        return f(*args, **kwargs)

    return wrapper
