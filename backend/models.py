from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Benutzer(db.Model):
    __tablename__ = 'benutzer'
    UserID = db.Column(db.Integer, primary_key=True)
    Vorname = db.Column(db.String(50))
    Nachname = db.Column(db.String(50))
    Email = db.Column(db.String(100), unique=True)
    PasswortHash = db.Column(db.String(255))
    Registrierungsdatum = db.Column(db.DateTime)
    LetzterLogin = db.Column(db.DateTime)
    Rolle = db.Column(db.String(20))

class Umfrage(db.Model):
    __tablename__ = 'umfrage'
    SurveyID = db.Column(db.Integer, primary_key=True)
    Titel = db.Column(db.String(100))
    Beschreibung = db.Column(db.Text)
    Erstellungsdatum = db.Column(db.DateTime)
    Startdatum = db.Column(db.DateTime)
    Enddatum = db.Column(db.DateTime)
    Status = db.Column(db.String(20))
    UserID = db.Column(db.Integer, db.ForeignKey('benutzer.UserID'))

    fragen = db.relationship("Frage", backref="umfrage", lazy=True)

class Frage(db.Model):
    __tablename__ = 'frage'
    QuestionID = db.Column(db.Integer, primary_key=True)
    Fragetext = db.Column(db.Text)
    Reihenfolge = db.Column(db.Integer, nullable=True)
    SurveyID = db.Column(db.Integer, db.ForeignKey('umfrage.SurveyID'))

    antwortoptionen = db.relationship("Antwortoption", backref="frage", lazy=True)

class Antwortoption(db.Model):
    __tablename__ = 'antwortoption'
    OptionID = db.Column(db.Integer, primary_key=True)
    Optionstext = db.Column(db.String(255))
    Reihenfolge = db.Column(db.Integer, nullable=True)
    QuestionID = db.Column(db.Integer, db.ForeignKey('frage.QuestionID'))

class Antwort(db.Model):
    __tablename__ = 'antwort'
    ResponseID = db.Column(db.Integer, primary_key=True)
    Antwortdatum = db.Column(db.DateTime)
    SurveyID = db.Column(db.Integer, db.ForeignKey('umfrage.SurveyID'))
    UserID = db.Column(db.Integer, db.ForeignKey('benutzer.UserID'))
    QuestionID = db.Column(db.Integer, db.ForeignKey('frage.QuestionID'))
    OptionID = db.Column(db.Integer, db.ForeignKey('antwortoption.OptionID'), nullable=True)

