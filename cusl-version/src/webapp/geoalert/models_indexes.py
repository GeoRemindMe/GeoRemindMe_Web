from google.appengine.ext import db

from models_list import *
from models import *


""" QUIZAS SERIA MEJOR LLEVAR LAS INVITACIONES ACEPTADAS COMO UNA LISTA Y NO CREAR UNA NUEVA INSTANCIA POR CADA LISTA
class InvitacionAceptadaIndex(db.Model):
    recomendacion = db.ReferenceProperty(Recomendacion)
    users = db.ListProperty(db.Key)
""" 
    
class Invitation(db.Model):
    """Por cada invitacion, se crea una nueva instancia"""
    sender = db.ReferenceProperty(User)
    to = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.IntegerProperty(default=0)