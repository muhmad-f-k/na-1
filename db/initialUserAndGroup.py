from db.modul import *


def create_initial_user_and_group():
    if not session.query(User).filter(User.id == 1).first():
        session.close()
        try:
            firstuser = User(email='mikal95@live.no',
                             first_name='Mikal',
                             last_name='Eriksen',
                             password_hash=generate_password_hash('123', method="sha256"))
            session.add(firstuser)
            session.commit()
            session.close()
        except:
            pass

        try:
            firstgroup = Group(name='Resturant Matmons')
            session.add(firstgroup)
            session.commit()
            session.close()
        except:
            pass

        try:
            admin = Role(name='admin')
            session.add(admin)
            session.commit()
            session.close()
        except:
            pass

        try:
            moderator = Role(name='moderator')
            session.add(moderator)
            session.commit()
            session.close()
        except:
            pass

        try:
            kokk = Role(name='kokk')
            session.add(kokk)
            session.commit()
            session.close()
        except:
            pass

        try:
            gjest = Role(name='gjest')
            session.add(gjest)
            session.commit()
            session.close()
        except:
            pass

        try:
            user = session.query(User).filter(User.id == 1).first()
            session.close()

            group = session.query(Group).filter(Group.name == 'Resturant Matmons').first()
            session.close()

            role = session.query(Role).filter(Role.name == "admin").first()
            session.close()

            firstUser_group_role = User_group_role(user=user, group=group, role=role)
            session.add(firstUser_group_role)
            session.commit()
            session.close()
        except:
            pass


create_initial_user_and_group()
