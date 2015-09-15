from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ascentio-test.db'
db = SQLAlchemy(app)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

#class Operation(db.Model): 
#    pass

@app.route("/")
def main():
    return "hola"

@app.route("/test/<path:aaa>")
def a_test_function(aaa):
   return "asdasdsa %s" % aaa

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

