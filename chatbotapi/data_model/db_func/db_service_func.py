import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from model_db import Services, Session

session = Session()

def getAllServices():
    services = session.query(Services).all()
    session.commit()
    return services