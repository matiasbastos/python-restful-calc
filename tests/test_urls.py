import pytest
import json
from .conftests import testapp

@pytest.mark.usefixtures("testapp")
class TestUrls:
    def test_add_calc(self, testapp):
        r = testapp.post('/calcs',
            data = {'input': 'log2'}, 
        )
        assert r.status_code == 201
        assert json.loads(r.data.decode("utf-8")) == {'output': 0.6931471805599453}

    def test_get_current_calcs(self, testapp):
        r = testapp.post('/calcs',
            data = {'input': 'log2'}, 
        )
        assert r.status_code == 201
        r = testapp.get('/calcs')
        assert r.status_code == 200
        d = json.loads(r.data.decode("utf-8"))
        assert d == {'current_session_calcs': [{'input': 'log2', 'output': 0.6931471805599453}]}

    def test_get_clean_current_calcs(self, testapp):
        r = testapp.post('/calcs',
            data = {'input': 'log2'}, 
        )
        assert r.status_code == 201
        r = testapp.get('/calcs')
        assert r.status_code == 200
        r = testapp.delete('/calcs')
        assert r.status_code == 200
        r = testapp.get('/calcs')
        assert r.status_code == 400

    def test_save_session(self, testapp):
        r = testapp.post('/calcs',
            data = {'input': 'log2'}, 
        )
        assert r.status_code == 201
        r = testapp.post('/sessions/testsession')
        assert r.status_code == 201
        d = json.loads(r.data.decode("utf-8"))
        assert d == {'message': 'Session saved. id: 1, name: testsession'}

    def test_get_session(self, testapp):
        r = testapp.post('/calcs',
            data = {'input': 'log2'}, 
        )
        assert r.status_code == 201
        r = testapp.post('/sessions/testsession')
        assert r.status_code == 201
        r = testapp.get('/sessions/testsession')
        assert r.status_code == 200
        d = json.loads(r.data.decode("utf-8"))
        assert d == {'session': {'id': 1,
                                 'name': 'testsession',
                                 'operations': [{'id': 1,
                                                 'input': 'log2',
                                                 'output': '0.693147180559945'}]}}

    def test_get_sessions(self, testapp):
        r = testapp.post('/calcs',
            data = {'input': '2+2'}, 
        )
        assert r.status_code == 201
        r = testapp.post('/calcs',
            data = {'input': 'log2'}, 
        )
        assert r.status_code == 201
        r = testapp.post('/sessions/testsession')
        assert r.status_code == 201
        r = testapp.get('/sessions')
        assert r.status_code == 200
        d = json.loads(r.data.decode("utf-8"))
        assert d == {'sessions': [{'id': 1,
                                   'name': 'testsession',
                                   'operations': [{'id': 1, 'input': '2+2', 'output': '4'},
                                                  {'id': 2,
                                                   'input': 'log2',
                                                   'output': '0.693147180559945'}]}]}
