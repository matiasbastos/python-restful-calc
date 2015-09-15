from flask import Flask, session, request, abort, jsonify
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
    
@app.route("/calc", methods = ["POST"])
def calc():
    if not request.form.get('input', False):
        abort(400)
    if 'calcs' not in session:
        session['calcs'] = []
    calc = {'input': request.form['input'], 
            'output': eval(request.form['input'])
    }
    session["calcs"].append(calc)
    return jsonify({'output': calc['output'], 'calcs': session["calcs"]})

@app.route("/persist/<string:session_name>")
def persist(session_name):    
    if 'calcs' in session:
        s = Session(session_name)
        db.session.add(s)
        for calc in session['calcs']:
            c = Operation(session=s, input=calc.input, output=calc.output)
            db.session.add(c)
        db.session.commit()
    return jsonify({'result': "moortaaal!"})

@app.route("/<string:session_name>")
def get_session(session_name):    
    return "hola"

app.secret_key = 'aafeb9552c67474e9b6ce85f0394aab1'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

