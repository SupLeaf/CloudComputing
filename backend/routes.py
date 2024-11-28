from flask import Blueprint, jsonify, request
from models import db, Umfrage, Frage, Antwort, Antwortoption
from schemas import UmfrageSchema, FrageSchema
from datetime import datetime

routes = Blueprint("routes", __name__)

@routes.route('/umfragen', methods=['GET'])                 #Gibt eine Liste der Umfragen und ihrer SurveyID's zurück
def get_umfragen():
    umfragen = Umfrage.query.all()
    umfrage_schema = UmfrageSchema(many=True)
    return jsonify(umfrage_schema.dump(umfragen))


@routes.route('/fragen/<int:survey_id>', methods=['GET'])   #Gibt eine Frage und ihre Antwortmöglichkeiten zurück
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

    return jsonify({"message": "Antwort gespeichert!"}), 201
