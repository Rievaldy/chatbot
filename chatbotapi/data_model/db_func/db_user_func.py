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
from model_db import User,Brand, Product, Services, Company,Maintenance,Session

session = Session()

def extract_explainer(text):
    regex = re.compile(r'\'[\w\@\.]+\'')
    value = re.findall(regex, text)
    message = value[0] +" already exist please use different "+value[1]
    return message

def insertUserData(name_user, email_user, password_user, phone_number, address_user,id_company):
    newUser = User(name_user=name_user, email_user=email_user,password_user=password_user, address_user=address_user, phone_number=phone_number, id_company=id_company)
    message = ""
    try:
        session.add(newUser)
        session.commit()
    except IntegrityError as e:
        code = e.orig.args[0]
        explain = e.orig.args[1]
        if code == 1062 : 
            message = extract_explainer(explain)
        session.rollback()
        return message,newUser
    else:
        return "Register Success", newUser

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
    message = ""
    try:
        session.commit()
    except SQLAlchemyError as e :
        message = e.__cause__
        return message, user
    else :
        if user is not None :
            message =  "user found"
        else :
             message = "not found"
        return message, user

def userLogin(email_user, password_user):
    user = session.query(User).filter(User.email_user == email_user and User.password_user == password_user).first()
    session.commit()
    if user is not None : message =  "Login Success"
    else : message = "Unable to find with given Email and Password"
    return message, user
            
print(User.__table__.columns.keys())