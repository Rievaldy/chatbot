from sqlalchemy import Table, Column, Integer, ForeignKey,String, DateTime
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:@localhost:3306/iprotect')
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

class Company(Base):
    __tablename__ = 'company'

    id_company = Column(mysql.INTEGER(4), primary_key=True)
    name_company = Column(String(50), nullable=False)
    address_company = Column(String(150), nullable=False)
    email_company = Column(String(30),unique=True, nullable=False)
    user = relationship('User', lazy = True)

    def __init__(self, name_company, address_company, email_company) :
        self.name_company = name_company
        self.address_company = address_company
        self.email_company = email_company

class User(Base):
    __tablename__ = 'user'

    id_user = Column(mysql.INTEGER(8), primary_key=True)
    name_user = Column(String(50), nullable=False)
    address_user = Column(String(150), nullable=False)
    email_user = Column(String(30),unique = True, nullable=False)
    password_user = Column(String(30), nullable=False)
    phone_number = Column(String(30),unique = True, nullable=False)
    id_company = Column(ForeignKey('company.id_company'), nullable = False)
    isLogin = Column(mysql.INTEGER(1),nullable=False)
    subscribeproduct = relationship('SubscribeProduct', lazy = True)
    maintenance = relationship('Maintenance', lazy = True)
    

    def __init__(self, name_user, address_user, email_user, password_user,phone_number,id_company) :
        self.name_user = name_user
        self.address_user = address_user
        self.email_user = email_user
        self.password_user = password_user
        self.phone_number = phone_number
        self.id_company = id_company



class Services(Base):
    __tablename__ = 'services'

    id_services = Column(mysql.INTEGER(1) ,primary_key=True)
    name_services = Column(String(50), nullable=False)
    desc_services = Column(String(500), nullable=False)
    brand = relationship('Brand', lazy = True)

    def __init__(self, name_service, desc_service) :
        self.name_service = name_service
        self.desc_service = desc_service

class Brand(Base):
    __tablename__ = 'brand'

    id_brand = Column(mysql.INTEGER(8), primary_key=True)
    name_brand = Column(String(25), nullable=False)
    desc_brand = Column(String(500), nullable=False)
    subscribeproduct = relationship('SubscribeProduct', lazy = True)
    subscribeproduct = relationship('Product', lazy = True)
    id_services = Column(mysql.INTEGER(1), ForeignKey('services.id_services'), nullable = False)

    def __init__(self, name_brand, desc_brand, id_services) :
        self.name_brand = name_brand
        self.desc_brand = desc_brand
        self.id_services = id_services

    def getName(self):
        return self.name_brand

class Product(Base):
    __tablename__ = 'product'

    id_product = Column(mysql.INTEGER(2), primary_key=True)
    name_product = Column(String(25), nullable=False)
    desc_product = Column(String(500), nullable=False)
    id_brand = Column(mysql.INTEGER(8), ForeignKey('brand.id_brand'), nullable = False)

    def __init__(self, name_product, desc_product, id_brand) :
        self.name_product = name_product
        self.desc_product = desc_product
        self.id_brand = id_brand

class Maintenance(Base):
    __tablename__ = 'maintenance'

    id_maintenance = Column(mysql.INTEGER(8), primary_key=True)
    id_user = Column(mysql.INTEGER(8), ForeignKey('user.id_user'), nullable = False)
    id_subcribe_product = Column(mysql.INTEGER(4), ForeignKey('subscribe_product.id_subcribe_product'), nullable = False)
    desc_maintenance = Column(String(150), nullable=False)
    request_date = Column(DateTime, default=datetime.datetime.utcnow)
    finish_date = Column(DateTime, nullable=True)
    severity_level = Column(mysql.INTEGER(1), nullable=False)
    status_code = Column(mysql.INTEGER(1), nullable=False)


    def __init__(self, id_user, id_subscribe_product, desc_maintenance,finish_date,severity_level,status_code) :
        self.id_user = id_user
        self.id_subscribe_product = id_subscribe_product
        self.desc_maintenance = desc_maintenance
        self.finish_date = finish_date
        self.severity_level = severity_level
        self.status_code = status_code

class SubscribeProduct(Base):
    __tablename__ = 'subscribe_product'

    id_subcribe_product = Column(mysql.INTEGER(4), primary_key=True)
    id_user = Column(mysql.INTEGER(8), ForeignKey('user.id_user'), unique=True, nullable = False)
    id_brand = Column(mysql.INTEGER(8),  ForeignKey('brand.id_brand'),unique=True, nullable = False)
    maintenance_ticket = Column(mysql.INTEGER(8),  ForeignKey('brand.id_brand'), nullable = True)
    request_date = Column(DateTime, default=datetime.datetime.utcnow , nullable = True)
    start_date = Column(DateTime , nullable = True)
    end_date = Column(DateTime , nullable = True)
    status_code = Column(mysql.INTEGER(1), nullable=False)
    subscribeproduct = relationship('Maintenance', lazy = True)

    def __init__(self, id_user, id_brand ,status_code) :# , maintenance_ticket, request_date, start_date,end_date,
        self.id_user = id_user
        self.id_brand = id_brand
        #self.maintenance_ticket = maintenance_ticket
        #self.request_date = request_date
        #self.start_date = start_date
        #self.end_date = end_date
        self.status_code = status_code


# db.drop_all()
# db.create_all()