from flask import Blueprint, render_template
from comment.forms import postCommentForm, editCommentForm
from modul import *

comment = Blueprint('comment', __name__)


@comment.route('/post_comment', methods=['GET', 'POST'])
def postComment():
    form = postCommentForm()
    if form.validate():
        user_id = 1
        dinner_id = 1
        comment_object = Comment(text=form.commentText.data, user_id=user_id, dinner_id=dinner_id)
        session.add(comment_object)
        session.commit()
        session.close()
    return render_template('postComment.html', form=form)


@comment.route('/edit_comment', methods=['GET', 'POST'])
def editComment(comment_id):
    editComment=session.query(comment).filter(comment_id==comment_id).first()
        session.delete(comment_id)
        session.commit()
