from db import *

# def db_edit_comment(mp_comment_id, mp_comment_text):
#     incoming_comment = session.query(Comment).filter(Comment.id == mp_comment_id).first()
#     incoming_dinner.title = mp_dinner_title
#     incoming_dinner.user_id = mp_dinner_user_id
#     incoming_dinner.group_id = mp_dinner_group_id
#     incoming_dinner.image = mp_dinner_image
#     session.commit()
#     session.close()


def db_new_comment(db_comment_text, db_user_id, db_dinner_id):
    comment = Comment(text=db_comment_text,
                      user_id=db_user_id, dinner_id=db_dinner_id)
    session.add(comment)
    session.commit()
    session.close()


def db_edit_comment(db_comment_id, db_comment_text):
    incoming_comment = session.query(Comment).filter(
        db_comment_id == Comment.id).first()
    to_mp_edited_comment = Edited_comment(
        comment_id=db_comment_id, text=incoming_comment.text)
    incoming_comment.text = db_comment_text
    session.add(to_mp_edited_comment)
    session.commit()
    session.close()


def db_delete_comment(mp_comment_id):
    session.query(Comment).filter_by(id=mp_comment_id).delete()
    session.commit()
    session.close()
