from functools import wraps

import sqlalchemy as sa
from flask import abort, flash, redirect, render_template, request, session, url_for

from app import db
from app.auth import bp
from app.models import Roles, Users


# This decorator was taken from the official Flask documentation
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "current_user" in session:
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "admin" in session["current_user"]["role"]:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


# ---- ROUTES ---- #
# --- AUTHENTICATION --- #
@bp.route("/register", methods=["GET", "POST"])
def register():
    """Seite zur Account-Erstellung"""
    role_user = db.session.scalar(sa.select(Roles).where(Roles.role == "user"))
    if request.method == "POST":
        # -- FORM VALIDATION -- #
        username = request.form.get("Username")
        password = request.form.get("Password")
        password_repeat = request.form.get("Password-Repeat")
        # check required fields
        if username == "" or password == "" or password_repeat == "":
            flash("Netter Versuch, so klappt das aber nicht.", "error")
        elif password != password:
            flash("Die Passworteingabe stimmt nicht überein", "error")
        # -- DATABASE HANDLING -- #
        else:
            username = username.lower()
            user = db.session.scalar(sa.select(Users).where(Users.username == username))
            if user is None:
                user = Users(username=username, role_id=role_user.role_id)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                user.login()
                flash("Glückwunsch! Du bist jetzt registriert.", "success")
                return redirect(url_for("main.index"))
            else:
                flash(
                    "Diesen Benutzer gibt es bereits, bitte wähle einen anderen Benutzernamen.",
                    "error",
                )
    return render_template("auth/register.html", current_user=None)


@bp.route("/logout")
@login_required
def logout():
    """Leer; wird für den Logout benötigt"""
    session.pop("current_user", None)
    return redirect(url_for("auth.login", next=request.url))
