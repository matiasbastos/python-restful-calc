from calc import create_app


class TestConfig:
    def test_dev_config(self):
        """ Tests if the development config loads correctly """

        app = create_app('calc.settings.DevConfig', env='dev')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../ascentio-test.db'

    def test_test_config(self):
        """ Tests if the test config loads correctly """

        app = create_app('calc.settings.TestConfig', env='dev')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_ECHO'] is True

    def test_prod_config(self):
        """ Tests if the production config loads correctly """

        app = create_app('calc.settings.ProdConfig', env='prod')

        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../ascentio-test.db'
