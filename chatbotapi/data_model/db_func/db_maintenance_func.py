import sys
import os.path
from sqlalchemy.exc import IntegrityError

from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import Maintenance, Company, User ,Session


session = Session()

def insertMaintenance(id_user, id_subcribe_product, desc_maintenance ,severity_level, status_code):
    newMaintenance = Maintenance(id_user=id_user, id_subcribe_product=id_subcribe_product, desc_maintenance=desc_maintenance, severity_level=severity_level, status_code=status_code)
    try:
        session.add(newMaintenance)
        session.commit()
    except IntegrityError as e :
        session.rollback()
        explain = e.orig.args[1]
        print(explain)
        return None
    else: return newMaintenance
    

def updateMaintenance(id_subscribe_product, field_name, value):
    maintenance = session.query(Maintenance).filter(Maintenance.id_subscribe_product == id_subscribe_product)
    maintenance.update({field_name : value})
    session.commit() 

def deleteMaintenance(id_subscribe_product):
    subscribe_product = session.query(Maintenance).filter(Maintenance.id_subscribe_product == id_subscribe_product)
    subscribe_product.delete()
    session.commit()

def getMaintenanceHistory():
    subscribe_product = session.query(Maintenance).all()
    session.commit()
    return subscribe_product

def getAllMaintenanceByIdSubscribe(id_subcribe_product):
    subscribe_product = session.query(Maintenance).join(User, User.id_user == Maintenance.id_user).filter(Maintenance.id_subcribe_product == id_subcribe_product, Maintenance.status_code == 1).all()
    session.commit()
    
    return subscribe_product

def getSpecificMaintenance(id_subcribe_product, request_date):
    subscribe_product = session.query(Maintenance,User).join(User, User.id_user == Maintenance.id_user).filter(Maintenance.id_subcribe_product == id_subcribe_product , Maintenance.request_date == request_date).first()
    session.commit()
    
    return subscribe_product


