import sys
import os.path
import re

from sqlalchemy.exc import IntegrityError
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import Company,Session

session = Session()


def extract_explainer(text):
    regex = re.compile(r'\'[\w\@\.]+\'')
    value = re.findall(regex, text)
    message = value[0] +" already exist please use different "+value[1]
    return message

def insertCompanyData(name_company, address_company, email_company):
    newCompany = Company(name_company=name_company, address_company=address_company,email_company=email_company)
    try:
        session.add(newCompany)
        session.commit()
    except IntegrityError as e:
        code = e.orig.args[0]
        explain = e.orig.args[1]
        if code == 1062 : 
            message = extract_explainer(explain)
        session.rollback()
        return message,newCompany
    else:
        return "Register Success", newCompany

def updateCompanyData(id_company, field_name, value):
    company = session.query(Company).filter(Company.id_company == id_company)
    company.update({field_name : value})
    session.commit()
    return company

def deleteCompanyData(id_company):
    company = session.query(Company).filter(Company.id_company == id_company)
    company.delete()
    session.commit()
    return company

def getAllCompany():
    company = session.query(Company).all()
    session.commit()
    return company
