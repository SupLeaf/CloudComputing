from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models import db, Umfrage, Frage, Antwort, Antwortoption
from schemas import UmfrageSchema, FrageSchema
from datetime import datetime, timedelta
import random

routes = Blueprint("routes", __name__)
CORS(routes)

#Gibt eine Liste der Umfragen und ihrer SurveyID's zurück
@routes.route('/umfragen', methods=['GET'])                 
def get_umfragen():
    umfragen = Umfrage.query.all()
    umfrage_schema = UmfrageSchema(many=True)
    return jsonify(umfrage_schema.dump(umfragen))


#Gibt eine Frage und ihre Antwortmöglichkeiten zurück
@routes.route('/fragen/<int:survey_id>', methods=['GET'])   
def get_fragen(survey_id):
    fragen = Frage.query.filter_by(SurveyID=survey_id).all()
    result = []
    for frage in fragen:
        frage_data = FrageSchema().dump(frage)
        antwortoptionen = Antwortoption.query.filter_by(QuestionID=frage.QuestionID).all()
        frage_data['Antwortoptionen'] = [{'OptionID': option.OptionID, 'Optionstext': option.Optionstext} for option in antwortoptionen]
        result.append(frage_data)
    return jsonify(result)



#Nimmt das Formular einer Abgegebenen Antwort an
    #z.b. in der Form:
    # {
    # "SurveyID": 1,
    # "UserID": 2,
    # "QuestionID": 1,
    # "OptionID": 3
    # }
@routes.route('/antwort', methods=['POST'])                 
def post_antwort():
    data = request.json
    max_response_id = db.session.query(db.func.max(Antwort.ResponseID)).scalar()
    antwort = Antwort(
        ResponseID = (max_response_id + 1) if max_response_id is not None else 1,
        Antwortdatum=datetime.now(),
        SurveyID=data['SurveyID'],
        UserID=data.get('UserID'),
        QuestionID=data['QuestionID'],
        OptionID=data['OptionID']
    )
    db.session.add(antwort)
    db.session.commit()

    response = jsonify({"message": "Antwort gespeichert!"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response, 201


#Fragt die Datenbank nach einer neuen uniquen SurveyID
#ACHTUNG: Reserviert noch kein Objekt in der Datenbank, da dafür ganze Umfrage angelegt werden muss
@routes.route('/getNewSurveyID', methods=['GET'])           
def get_new_SurveyID():
    def generate_unique_survey_id():
        while True:
            new_id = random.randint(1000, 9999)
            if not Umfrage.query.filter_by(SurveyID=new_id).first():
                return new_id

    new_survey_id = generate_unique_survey_id()
    return jsonify({"new_survey_id": new_survey_id})






# POST-Route zum Erstellen einer neuen Umfrage durch den Admin

@routes.route('/neueUmfrage', methods=['POST'])
def create_new_Survey():
    data = request.json
    survey = Umfrage(
        SurveyID=data['SurveyID'],
        Titel=data['Titel'],
        Beschreibung=data['Beschreibung'],
        Erstellungsdatum=datetime.now(),
        Startdatum=datetime.now(),
        Enddatum=datetime.now() + timedelta(days=365),
        Status=data['Status'],
        UserID=data['UserID']
    )
    db.session.add(survey)
    db.session.commit()

    for frage_data in data['Fragen']:
        max_question_id = db.session.query(db.func.max(Frage.QuestionID)).scalar()
        frage = Frage(
            QuestionID=(max_question_id + 1) if max_question_id is not None else 1,
            Fragetext=frage_data['Fragetext'],
            Reihenfolge=frage_data.get('Reihenfolge', None),
            SurveyID=survey.SurveyID
        )
        db.session.add(frage)
        db.session.commit()

        for antwortoption_data in frage_data['Antwortoptionen']:
            max_option_id = db.session.query(db.func.max(Antwortoption.OptionID)).scalar()
            antwortoption = Antwortoption(
                OptionID=(max_option_id + 1) if max_option_id is not None else 1,
                Optionstext=antwortoption_data['Optionstext'],
                Reihenfolge=antwortoption_data.get('Reihenfolge', None),
                QuestionID=frage.QuestionID
            )
            db.session.add(antwortoption)
    db.session.commit()

    return jsonify({"message": "Umfrage und Fragen erfolgreich erstellt!"}), 201
# Beispiel Anfrage in JSON:
# {
#     "SurveyID": 1,
#     "Titel": "Lieblingsfarbe Umfrage",
#     "Beschreibung": "Eine Umfrage über Lieblingsfarben",
#     "Status": "active",
#     "UserID": 1,
#     "Fragen": [
#         {
#             "QuestionID": 1,
#             "Fragetext": "Was ist deine Lieblingsfarbe?",
#             "Reihenfolge": 1,
#             "Antwortoptionen": [
#                 {
#                     "Optionstext": "Blau",
#                     "Reihenfolge": 1
#                 },
#                 {
#                     "Optionstext": "Gelb",
#                     "Reihenfolge": 2
#                 },
#                 {
#                     "Optionstext": "Rot",
#                     "Reihenfolge": 3
#                 },
#                 {
#                     "Optionstext": "Grün",
#                     "Reihenfolge": 4
#                 }
#             ]
#         }
#     ]
# }
#


@routes.route('/deleteUmfrage/<int:survey_id>', methods=['DELETE'])
def delete_umfrage(survey_id):
    # Find the survey by SurveyID
    survey = Umfrage.query.get(survey_id)
    if not survey:
        return jsonify({"message": "Survey not found"}), 404

    # Delete the survey (questions and answer options will be deleted automatically)
    db.session.delete(survey)
    db.session.commit()

    return jsonify({"message": "Survey and associated questions and answer options deleted successfully"}), 200