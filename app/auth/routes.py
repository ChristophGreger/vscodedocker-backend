from app.auth import auth
from flask import request, session


@auth.route("/login", methods=["POST"])
def hello():
    if request.form.get("password") == "password":
        session["logged_in"] = "True"
        return "Logged in", 200
    else:
        return "Invalid credentials", 401


@auth.route("/logout", methods=["POST"])
def logout():
    if session.get("logged_in"):
        session.pop("logged_in")
        return "Logged out", 200
    else:
        return "User Wasn't logged in", 400
