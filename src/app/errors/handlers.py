from flask import render_template, session

from app import db
from app.errors import bp


@bp.app_errorhandler(400)
def bad_request(error):
    """Behandelt die 400 Fehler"""
    return render_template("errors/400.html", current_user=session["current_user"]), 400


@bp.app_errorhandler(403)
def forbidden(error):
    """Behandelt die 403 Fehler"""
    return render_template("errors/403.html", current_user=session["current_user"]), 403


@bp.app_errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    return render_template("errors/404.html", current_user=session["current_user"]), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html", current_user=session["current_user"]), 500
