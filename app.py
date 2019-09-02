from flask import Flask, request, jsonify
import config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)  # restful

from models import *


class Polls(Resource):
    def post(self):
        data = request.get_json(force=True)
        poll = data["poll"]
        new_poll = Poll(name=poll['name'],
                        explanation=poll['explanation'])

        db.session.add(new_poll)
        db.session.commit()

        questions = data["poll"]["questions"]
        for i in range(len(questions)):
            new_question = Question(poll=new_poll,
                                    text=questions[i]["text"],
                                    type=questions[i]["type"])
            db.session.add(new_question)
            db.session.commit()

            answers = questions[i]["answers"]
            for j in range(len(answers)):
                new_answer = Answer(question=new_question,
                                    text=answers[j])
                db.session.add(new_answer)
                db.session.commit()

        return jsonify({'message': 'New poll created'})

    def get(self):
        all_polls = Poll.query.all()
        output = []

        for poll in all_polls:
            poll_data = {}
            poll_data["id"] = poll.id
            poll_data["name"] = poll.name
            poll_data["explanation"] = poll.explanation
            output.append(poll_data)

        return jsonify({"polls": output})





api.add_resource(Polls, '/poll')


if __name__ == '__main__':
    app.run(debug=True)
