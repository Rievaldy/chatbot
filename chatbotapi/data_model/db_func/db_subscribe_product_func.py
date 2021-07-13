import sys
import os.path

from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import SubscribeProduct, Company, User ,Session


session = Session()

def insertSubscribeProduct(id_user , id_brand, status_code):
    checkUserCompany = session.query(User).filter(User.id_user == id_user).first()
    checkduplicacte = session.query(User).join(SubscribeProduct).filter(User.id_company == checkUserCompany.id_company, SubscribeProduct.id_brand == id_brand).first()
    session.commit()
    message = ""
    if checkduplicacte != None : message = "1 of your colleague with name '"+ checkduplicacte.name_user+"' already requested the same product"
    else :
        newSubscribeProduct = SubscribeProduct(id_user=id_user, id_brand=id_brand, status_code=status_code)
        session.add(newSubscribeProduct)
        session.commit()
        message = "request product success"

    return message,newSubscribeProduct

def updateSubscribeProduct(id_subscribe_product, field_name, value):
    subscribe_product = session.query(SubscribeProduct).filter(SubscribeProduct.id_subscribe_product == id_subscribe_product)
    subscribe_product.update({field_name : value})
    session.commit() 

def deleteSubscribeProduct(id_subscribe_product):
    subscribe_product = session.query(SubscribeProduct).filter(SubscribeProduct.id_subscribe_product == id_subscribe_product)
    subscribe_product.delete()
    session.commit()

def getAllSubscribeProduct():
    subscribe_product = session.query(SubscribeProduct).all()
    session.commit()
    return subscribe_product

def getAlSubscribeProductByCompany(id_company):
    subscribe_product = session.query(SubscribeProduct).join(User).filter(User.id_company == id_company and SubscribeProduct.status_code == 0).all()
    session.commit()
    if len(subscribe_product) > 0 :
        return "product Found",subscribe_product
    else :
        return "product Not Found",subscribe_product
