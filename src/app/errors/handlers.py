from flask import render_template, session
from warnings import deprecated
from app import db
from app.errors import bp

@deprecated("use code provided in v0 instead.")
@bp.app_errorhandler(400)
def bad_request(error):
    """Behandelt die 400 Fehler"""
    return render_template("errors/400.html"), 400

@deprecated("use code provided in v0 instead.")
@bp.app_errorhandler(403)
def forbidden(error):
    """Behandelt die 403 Fehler"""
    return render_template("errors/403.html"), 403

@deprecated("use code provided in v0 instead.")
@bp.app_errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    return render_template("errors/404.html"), 404

@deprecated("use code provided in v0 instead.")
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500
