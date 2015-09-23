from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Session: %s" % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'operations': [i.serialize() for i in self.operations]
        }


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    session = db.relationship(
        'Session', backref=db.backref('operations', lazy='dynamic'))
    input = db.Column(db.String(255))
    output = db.Column(db.String(64))

    def __init__(self, session, input, output):
        self.session = session
        self.input = input
        self.output = output

    def __repr__(self):
        return "Operation %s: Input = %s, Output = %s" % (self.id, self.input, self.output)

    def serialize(self):
        return {
            'id': self.id,
            'input': self.input,
            'output': self.output
        }
