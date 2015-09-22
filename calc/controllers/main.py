from flask import Blueprint, session, request, abort, jsonify
from calc.models import db, Session, Operation 
from calc.parser import parse 

main = Blueprint('main', __name__)


@main.route("/calcs", methods = ["GET"])
def get_calcs():
    if 'calcs' in session:
        return jsonify({'current_session_calcs': session['calcs']})
    return abort(400, "No calcs in current session.")

@main.route("/calcs", methods = ["POST"])
def add_calc():
    if not request.form.get('input', False):
        return abort(400, 'No input parameter.')
    if 'calcs' not in session:
        session['calcs'] = []
    try:
        output = parse(request.form['input'])
    except Exception as e:
        return abort(500, str(e))
    calc = {'input': request.form['input'], 
            'output': output
    }
    session["calcs"].append(calc)
    return jsonify({'output': calc['output']}), 201

@main.route("/calcs", methods = ["DELETE"])
def del_current_calcs():
    session.pop('calcs', None)
    return jsonify({'message': "Calcs session cleaned."})

@main.route("/sessions", methods = ["GET"])
def get_sessions():
    try:
        s = Session.query.all()
        if not s:
            raise Exception("Nothing saved yet!")
        return jsonify({'sessions': [i.serialize() for i in s]})
    except Exception as e:
        return abort(500, "Error loading sessions: %s" % str(e))

@main.route("/sessions/<string:session_name>", methods = ["GET"])
def get_session(session_name):
    try:
        s = Session.query.filter_by(name=session_name).first()
        if not s:
            return abort(400, "Session name = %s not found." % session_name)
        calcs = Operation.query.filter_by(session_id=s.id).all()
        operations = []
        for calc in calcs:
            operations.append("Input: %s, Output: %s" % (calc.input, calc.output))
        return jsonify({'session': s.serialize()})
    except Exception as e:
        return abort(500, "Error loading session: %s" % str(e))

@main.route("/sessions/<string:session_name>", methods = ["POST"])
def save_session(session_name):    
    if 'calcs' in session:
        s = Session.query.filter_by(name=session_name).first()
        if s:
            return abort(500, "The session name '%s' already exists." % session_name)
        try:
            s = Session(session_name)
            db.session.add(s)
            for calc in session['calcs']:
                c = Operation(session=s, input=calc['input'], output=calc['output'])
                db.session.add(c)
            db.session.commit()
            session.pop('calcs', None)
            return jsonify({'message': "Session saved. id: %s, name: %s" % (s.id, s.name) }), 201
        except Exception as e:
            return abort(500, "Error while saving session: %s" % str(e))
    return abort(400, "Nothing to save.")
