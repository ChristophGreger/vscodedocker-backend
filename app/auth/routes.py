from app.auth import auth


@auth.route("/hello")
def hello():
    return "Hello, World!"
