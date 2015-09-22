import pytest
from .conftests import testapp
from calc.models import db, Session, Operation


@pytest.mark.usefixtures("testapp")
class TestModels:
    def test_session_save(self, testapp):
        """ Test Session model to the database """

        s = Session('sessionname')
        db.session.add(s)
        db.session.commit()

        s = Session.query.filter_by(name="sessionname").first()
        assert s is not None

    def test_operation_save(self, testapp):
        """ Test Operation model to the database """

        s = Session('sessionname')
        o = Operation(s, 'testinput', 'testoutput')
        db.session.add(s)
        db.session.add(o)
        db.session.commit()

        o = Operation.query.filter_by(session=s).first()
        assert o is not None
