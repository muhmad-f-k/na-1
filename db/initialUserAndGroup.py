from modul import *


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


def add_measurements():
    kg = Measurement(name="kg")
    g = Measurement(name="g")
    mg = Measurement(name="mg")
    l = Measurement(name="l")
    dl = Measurement(name="dl")
    cl = Measurement(name="cl")
    ml = Measurement(name="ml")
    ss = Measurement(name="ss")
    ts = Measurement(name="ts")
    stk = Measurement(name="stk")

    if not (session.query(Measurement).filter(Measurement.id).first()):
        session.add_all([kg, g, mg, l, dl, cl, ml, ss, ts, stk])
        session.commit()
        session.close()


create_initial_user_and_group()
add_measurements()