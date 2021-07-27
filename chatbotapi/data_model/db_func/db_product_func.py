import sys
import os.path

from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import Product,Brand, Session


session = Session()

def insertProductData(name_product, desc_product, id_brand):
    newProduct = Product(name_product = name_product, desc_product = desc_product, id_brand = id_brand)
    session.add(newProduct)
    session.commit()

    return newProduct

def updateProductData(id_product, field_name, value):
    product = session.query(Product).filter(Product.id_product == id_product)
    product.update({field_name : value})
    session.commit() 

def deleteProductData(id_product):
    product = session.query(Product).filter(Product.id_product == id_product)
    product.delete()
    session.commit()

def getAllProduct():
    product = session.query(Product,Brand).join(Brand, Brand.id_brand == Product.id_brand).order_by(Product.id_brand.asc()).all()
    session.commit()
    return product

def getAllProductByBrand(id_brand):
    product = session.query(Product).filter(Product.id_brand == id_brand ).all()
    session.commit()
    return product

def getDetailProduct(id_product):
    product = session.query(Product).filter(Product.id_product == id_product).first()
    session.commit()
    return product


products = getAllProduct()

for product in products :
    print(str(product[0].name_product) + " --- "+ str(product[1].name_brand))