import sys
import os.path
from sqlalchemy.exc import IntegrityError

from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import SubscribeProduct, Company, User, Product,Brand ,Session


session = Session()

def insertSubscribeProduct(id_user,id_company , id_product, status_code):
    newSubscribeProduct = SubscribeProduct(id_user=id_user,id_company=id_company, id_product=id_product, status_code=status_code)
    try:
        session.add(newSubscribeProduct)
        session.commit()     
    except IntegrityError as e:
        Session.rollback()
        code = e.orig.args[0]
        print(code)    
        return None
    else : return newSubscribeProduct
    

def updateSubscribeProduct(id_subscribe_product, field_name, value):
    subscribe_product = session.query(SubscribeProduct).filter(SubscribeProduct.id_subscribe_product == id_subscribe_product)
    subscribe_product.update({field_name : value})
    session.commit() 

def deleteSubscribeProduct(id_subscribe_product):
    subscribe_product = session.query(SubscribeProduct).filter(SubscribeProduct.id_subscribe_product == id_subscribe_product)
    subscribe_product.delete()
    session.commit()

def getAllSubscribeProduct():
    subscribe_product = session.query(SubscribeProduct,User,Company,Product).join(User, User.id_user == SubscribeProduct.id_user).join(Company, Company.id_company == SubscribeProduct.id_company).join(Product, Product.id_product == SubscribeProduct.id_product).all()
    session.commit()
    print(subscribe_product[0][1].id_user)
    return subscribe_product

def getAlSubscribeProductByCompany(id_company):
    subscribe_product = session.query(SubscribeProduct, User, Company, Product).join(User, User.id_user == SubscribeProduct.id_user).join(Company, Company.id_company == SubscribeProduct.id_company).join(Product, Product.id_product == SubscribeProduct.id_product).filter(SubscribeProduct.id_company == id_company , SubscribeProduct.status_code == 1).all()
    session.commit()
    if len(subscribe_product) > 0 :
        return subscribe_product
    else :
        return None

def getSubscribeProductByIdSubscribe(id_subcribe_product):
    subscribe_product = session.query(SubscribeProduct, User, Company, Product,Brand).join(User, User.id_user == SubscribeProduct.id_user).join(Company, Company.id_company == SubscribeProduct.id_company).join(Product, Product.id_product == SubscribeProduct.id_product).join(Brand, Brand.id_brand == Product.id_brand).filter(SubscribeProduct.id_subcribe_product == id_subcribe_product).first()
    session.commit()
    return subscribe_product





