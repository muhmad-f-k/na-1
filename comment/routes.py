from flask import Blueprint, render_template, flash
from comment.forms import *
from comment.queries import *
from modul import *

comment = Blueprint('comment', __name__)


@comment.route('/post_comment', methods=['GET', 'POST'])
def post_comment():
    form = postCommentForm()
    if form.validate():
        user_id = 1
        dinner_id = 1
        db_new_comment(form.commentText.data, user_id, dinner_id)
    return render_template('postComment.html', form=form)


# @comment.route('/edit_comment', methods=['GET', 'POST'])
# def editComment(comment_id):
#     comment_id = 1
#     editComment=session.query(comment).filter(comment_id==comment_id).first()
#         session.delete(comment_id)
#         session.commit()

# SELECT * FROM kommentar WHERE kommentar_id =(%s)", (kommentar_id,)
# DELETE FROM kommentar WHERE kommentar_id=(%s)", (kommentar_id,)

@comment.route('/edit_comment', methods=['GET', 'POST'])
def edit_comment():
    comment_id = 1
    form = editCommentForm()
    if form.validate_on_submit():
        db_edit_comment(comment_id, form.commentText.data)
        flash(f'kommentar oppdatert!')
    return render_template('commentTemplates/edit_Comment.html', form=form)


@comment.route('/delete_comment',  methods=['GET', 'POST'])
def delete_comment():
    form = DeleteCommentForm()
    if form.validate_on_submit():
        db_delete_comment(form.mp_comment_id.data)
        flash(f'Kommentar slettet!')
    return render_template('commentTemplates/deleteComment.html', form=form)