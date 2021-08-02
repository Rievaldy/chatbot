import sys
import os.path

from sqlalchemy.sql.expression import null
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import ChatHistory, Session


session = Session()

def insertChatHistory(id_user, user_input, chatbot_response ,desc_tag, status_desc):
    newChatHistory = ChatHistory(id_user=id_user, user_input=user_input, chatbot_response=chatbot_response, desc_tag=desc_tag, status_desc=status_desc)
    session.add(newChatHistory)
    session.commit()

    return newChatHistory

'''def updateChatHistory(id_brand, field_name, value):
    brand = session.query(Brand).filter(Brand.id_brand == id_brand)
    brand.update({field_name : value})
    session.commit() 

def deleteChatHistory(id_brand):
    brand = session.query(Brand).filter(Brand.id_brand == id_brand)
    brand.delete()
    session.commit()

def getChatHistory():
    brand = session.query(Brand).all()
    session.commit()
    return brand
'''
