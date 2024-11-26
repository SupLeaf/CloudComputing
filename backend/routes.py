from flask import Blueprint, jsonify, request
from models import db, Umfrage, Frage, Antwort, Antwortoption
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
        UserID=data.get('UserID'),
        details=data['details']  # Store details directly in Antwort
    )
    db.session.add(antwort)
    db.session.commit()
    return jsonify({"message": "Antwort gespeichert!"}), 201

@routes.route('/antwortdetails/<int:response_id>', methods=['GET'])
def get_antwortdetails(response_id):
    antwort = Antwort.query.filter_by(ResponseID=response_id).first()
    result = []
    if antwort:
        for detail in antwort.details:
            option = Antwortoption.query.filter_by(OptionID=detail.get('OptionID')).first()
            frage = Frage.query.filter_by(QuestionID=detail['QuestionID']).first()
            entry = {}
            if frage and frage.Fragetext:
                entry['Fragetext'] = frage.Fragetext
            if option and option.Optionstext:
                entry['Optionstext'] = option.Optionstext
            if detail.get('Freitextantwort'):
                entry['Freitextantwort'] = detail['Freitextantwort']
            if entry:
                result.append(entry)
    return jsonify(result)

