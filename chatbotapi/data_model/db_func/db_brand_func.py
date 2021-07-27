import sys
import os.path

from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import Brand, Session


session = Session()

def insertBrandData(name_brand, desc_brand, id_services):
    newBrand = Brand(name_brand=name_brand, desc_brand=desc_brand,id_services=id_services)
    session.add(newBrand)
    session.commit()

    return Brand(newBrand)

def updateBrandData(id_brand, field_name, value):
    brand = session.query(Brand).filter(Brand.id_brand == id_brand)
    brand.update({field_name : value})
    session.commit() 

def deleteBrandData(id_brand):
    brand = session.query(Brand).filter(Brand.id_brand == id_brand)
    brand.delete()
    session.commit()

def getAllBrand():
    brand = session.query(Brand).all()
    session.commit()
    return brand

def searchSpecificBrand(id_brand):
    brand = session.query(Brand).filter(Brand.id_brand == id_brand).first()
    session.commit()
    print(brand.name_brand)
    if brand is not None :
        return "Brand Found",brand
    else :
        return "Brand Not Found",brand

brand = getAllBrand()

for bran in brand :
    print(bran.name_brand)