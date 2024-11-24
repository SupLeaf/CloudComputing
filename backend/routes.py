from flask import Blueprint, jsonify, request
from models import db, Umfrage, Frage, Antwort, Antwortdetail
from schemas import UmfrageSchema, FrageSchema

routes = Blueprint("routes", __name__)

@routes.route('/umfragen', methods=['GET'])
def get_umfragen():
    umfragen = Umfrage.query.all()
    umfrage_schema = UmfrageSchema(many=True)
    return jsonify(umfrage_schema.dump(umfragen))

@routes.route('/fragen/<int:survey_id>', methods=['GET'])
def get_fragen(survey_id):
    fragen = Frage.query.filter_by(SurveyID=survey_id).all()
    frage_schema = FrageSchema(many=True)
    return jsonify(frage_schema.dump(fragen))

@routes.route('/antwort', methods=['POST'])
def post_antwort():
    data = request.json
    antwort = Antwort(
        Antwortdatum=data['Antwortdatum'],
        SurveyID=data['SurveyID'],
        UserID=data.get('UserID')
    )
    db.session.add(antwort)
    db.session.commit()

    for detail in data['details']:
        antwortdetail = Antwortdetail(
            ResponseID=antwort.ResponseID,
            QuestionID=detail['QuestionID'],
            OptionID=detail.get('OptionID'),
            Freitextantwort=detail.get('Freitextantwort')
        )
        db.session.add(antwortdetail)

    db.session.commit()
    return jsonify({"message": "Antwort gespeichert!"}), 201
