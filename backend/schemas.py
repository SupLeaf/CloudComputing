from flask_marshmallow import Marshmallow
from models import Benutzer, Umfrage, Frage, Antwortoption, Antwort

ma = Marshmallow()

class BenutzerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Benutzer

class UmfrageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Umfrage

class FrageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Frage

class AntwortoptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Antwortoption

class AntwortSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Antwort

