from flask import Blueprint, session, request, abort, jsonify
from calc.models import db, Session, Operation 
from calc.parser import parse 

main = Blueprint('main', __name__)


@main.route("/calc", methods = ["POST"])
def calc():
    if not request.form.get('input', False):
        return abort(400)
    if 'calcs' not in session:
        session['calcs'] = []
    try:
        output = parse(request.form['input'])
    except Exception as e:
        return abort(500)
    calc = {'input': request.form['input'], 
            'output': output
    }
    session["calcs"].append(calc)
    return jsonify({'output': calc['output'], 'calcs': session["calcs"]})

@main.route("/persist/<string:session_name>", methods = ["GET"])
def persist(session_name):    
    if 'calcs' in session:
        try:
            s = Session(session_name)
            db.session.add(s)
            for calc in session['calcs']:
                c = Operation(session=s, input=calc['input'], output=calc['output'])
                db.session.add(c)
            db.session.commit()
            return jsonify({'success': "Session (id: %s, name: %s) saved!" % (s.id, s.name) })
        except Exception as e:
            return jsonify({'error': "Error while saving session: %s." % str(e)})
    else:
        return jsonify({'error': "Nothing to save."})

@main.route("/<string:session_name>", methods = ["GET"])
def get_session(session_name):
    try:
        s = Session.query.filter_by(name=session_name).first()
        if not s:
            return abort(404)
        calcs = Operation.query.filter_by(session_id=s.id).all()
        operations = []
        for calc in calcs:
            operations.append("Input: %s, Output: %s" % (calc.input, calc.output))
        return jsonify({'operations': operations})
    except Exception as e:
        return jsonify({'error': "Error while saving session: %s." % str(e)})
