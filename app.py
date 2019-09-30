from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
api = Api(app)  # restful

from models import *


class Polls(Resource):
    def post(self):
        poll = request.get_json(force=True)
        new_poll = Poll(name=poll['name'],
                        explanation=poll['explanation'])

        db.session.add(new_poll)
        db.session.commit()

        questions = poll["questions"]
        for i in range(len(questions)):
            new_question = Question(poll=new_poll,
                                    text=questions[i]["text"],
                                    type=questions[i]["type"])
            db.session.add(new_question)
            db.session.commit()

            test_choices = questions[i]["testChoices"]
            for j in range(len(test_choices)):
                new_test_choice = TestChoice(question=new_question,
                                             text=test_choices[j]["text"])
                db.session.add(new_test_choice)
                db.session.commit()

        return jsonify({'message': 'New poll created'})

    def get(self):
        all_polls = Poll.query.all()
        output = []

        for poll in all_polls:
            new_poll = create_poll_data(poll)
            output.append(new_poll)

        return jsonify(output)


class Anket(Resource):
    def get(self, poll_id):
        poll = Poll.query.get(poll_id)
        output = create_poll_data(poll)
        return jsonify(output)


def create_poll_data(poll):
    poll_data = {"id": poll.id,
                 "name": poll.name,
                 "explanation": poll.explanation,
                 "questions": []}
    for question in poll.questions:
        question_data = {"id": question.id,
                         "text": question.text,
                         "type": question.type,
                         "test_choices": []}
        for choice in question.test_choices:
            choice_data = {"id": choice.id,
                           "text": choice.text}
            question_data["test_choices"].append(choice_data)
        poll_data["questions"].append(question_data)

    return poll_data


api.add_resource(Polls, '/poll')
api.add_resource(Anket, '/poll/<int:poll_id>')


if __name__ == '__main__':
    app.run(debug=True)
