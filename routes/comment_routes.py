
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user

from db.xmodul import Comment, session

comment = Blueprint('comment', __name__, template_folder="templates")


@comment.route("/post_comment")
def post_comment():
    return render_template("comment.html")


@comment.route("/post_comment", methods=['POST'])
@login_required
def post_comment_post():
    user_id = current_user.id
    dinner_id = request.args.get('dinner_id')
    text = request.form.get("comment")

    comment = Comment(user_id=user_id, dinner_id=dinner_id, text=text)
    session.add(comment)
    session.commit()
    session.close()

    return redirect(url_for(""))