from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ascentio-test.db'
db = SQLAlchemy(app)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name  = name

    def __repr__(self):
        return "Session: %s" % self.name

class Operation(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    session = db.relationship('Session', backref=db.backref('operations', lazy='dynamic'))
    input = db.Column(db.String(255))
    output = db.Column(db.String(64))

    def __init__(self, session, input, output):
        self.session = session
        self.input = input
        self.output = output

    def __repr__(self):
        return "Operation %s: Input = %s, Output = %s" % (self.id, self.input, self.output)
    
@app.route("/add_calc", method=["POST"])
def add_calc():
    return "hola"

@app.route("/persist")
def persist():    
    return "hola"

@app.route("/")
def get_session():    
    return "hola"

app.secret_key = 'aafeb9552c67474e9b6ce85f0394aab1'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

