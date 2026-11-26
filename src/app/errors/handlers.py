from flask import render_template, jsonify

from app import db
from app.errors import bp


@bp.app_errorhandler(400)
def bad_request(error):
    #return render_template("errors/400.html"), 400
    return jsonify({"messages":""}), 400


@bp.app_errorhandler(401)
def unauthorized(error):
    return jsonify({"messages":""}), 401


@bp.app_errorhandler(403)
def forbidden(error):
    #return render_template("errors/403.html"), 403
    return jsonify({"messages":""}), 403


@bp.app_errorhandler(404)
def page_not_found(error):
    #return render_template("errors/404.html"), 404
    return jsonify({"messages":""}), 404


@bp.app_errorhandler(409)
def conflict(error):
    #return render_template("errors/404.html"), 404
    return jsonify({"messages":""}), 409


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    #return render_template("errors/500.html"), 500
    return jsonify({"messages":""}), 500
