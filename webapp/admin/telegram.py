from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from webapp import db, telegram
from webapp.admin import bp
from webapp.admin.forms import TelegramBotForm


@bp.route("/telegram/toggle_telegram", methods=["GET", "POST"])
@login_required
def toggle_telegram():
    form = TelegramBotForm()
    if form.validate_on_submit():
        if form.toggle.data:
            telegram.enable_webhook(request.url_root[:-1] + url_for("telegram.update"))
        else:
            telegram.disable_webhook()
        flash("Successfully toggled Telegram Webhook!", "success")
        return redirect(url_for("admin.toggle_telegram"))
    return render_template("admin/telegram/toggle_telegram.html", form=form)
