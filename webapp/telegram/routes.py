import jwt
from flask import current_app, request
from flask_login import current_user
from webapp import db, telegram
from webapp.telegram import bp
from webapp.models import User


@bp.route("/update", methods=["POST"])
def update():
    message = telegram.parse_update(request.get_data())
    text = message["text"]
    if text.startswith("/register "):
        user_id_token = text.split("/register ")[1]
        user_id = jwt.decode(user_id_token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        user = User.query.get(user_id["user_id"])
        user.telegram_id = message["from"]["id"]
        db.session.commit()
        telegram.send_message(message["from"]["id"], "Dear {}, you've registered for telegram subscription!".format(user.profile.get_full_name()))
    elif text.startswith("/unregister"):
        user = User.query.filter_by(telegram_id=message["from"]["id"]).first()
        user.telegram_id = None
        db.session.commit()
        telegram.send_message(message["from"]["id"], "Dear {}, we're sad to see you leave :( come back soon!".format(user.profile.get_full_name()))
    return ""
