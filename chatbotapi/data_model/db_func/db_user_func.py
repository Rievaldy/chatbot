import sys
import os.path
import sqlalchemy
import re

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import User, Session
from model_db import User,Session

session = Session() 

def insertUserData(id_user, name_user, email_user, phone_number, address_user, id_company):
    newUser = User(id_user= id_user, name_user=name_user, email_user=email_user, address_user=address_user, phone_number=phone_number, id_company=id_company)
    try:
        session.add(newUser)
        session.commit()
    except IntegrityError as e:
        explain = e.orig.args[1]
        print(explain)
        return None
    else:
        return newUser

def updateUserData(id_user, field_name, value):
    user = session.query(User).filter(User.id_user == id_user)
    user.update({field_name : value})
    session.commit() 

def deleteUserData(id_user):
    user = session.query(User).filter(User.id_user == id_user)
    user.delete()
    session.commit()

def getUserData(id_user):
    user = session.query(User).filter(User.id_user == id_user).first()
    try:
        session.commit()
    except SQLAlchemyError as e :
        return None
    else :
        return user
        

def userLogin(email_user, password_user):
    user = session.query(User).filter(User.email_user == email_user and User.password_user == password_user).first()
    session.commit()
    if user is not None : message =  "Login Success"
    else : message = "Unable to find with given Email and Password"
    return message, user

