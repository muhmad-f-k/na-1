from db.modul import *


def add_roles():
    admin = Role(name="admin")
    moderator = Role(name="moderator")
    kokk = Role(name="kokk")
    gjest = Role(name="gjest")

    if not (session.query(Role).filter(Role.id).first()):
        session.add_all([admin, moderator, kokk, gjest])
        session.commit()
        session.close()


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


add_roles()
add_measurements()