# Python RESTful Calc

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

RESTful API en python para hacer cálculos matemáticos simples: suma, resta, multiplicación, division, potencia y logaritmo natural.

## Requerimientos
Escribir una calculadora simple con las siguientes funcionalidades:
- La calculadora debe soportar:
    - suma,  
    - resta,   
    - multiplicación,  
    - división,  
    - logaritmo con números de punto flotante. 
    - Ejemplo: (2+2)*log 10/3 
    - se tiene que poder persistir una sesión de cálculo. 
    - se tiene que poder recuperar una sesión de cálculo almacenada.
    - Ejemplo: 
        *input: 2+2
        *output: 4
        *input: 5*3*(8-23)
        *output: -225
        *input: guardar sesion1
        *output: sesion1 almacenada
        *input: recuperar sesion1
        *output: 2+2 = 4
                 5*3*(8-23) = -225

Idealmente el motor de cálculo de esta aplicación tendría que estar en un servidor de aplicaciones Python, con una base de persistencia liviana, como SQLite o una BD en memoria, y su interfaz tendría que ser REST o Web Service. 

## Solución
Para este proyecto opte por utilizar un microframework, [Flask](http://flask.pocoo.org/), ya que lo que necesito es solo exponer los endpoints por protocolo http y brindarle una estructura clara, testeable y eventualmente mantenible a la aplicación.
Para la persistencia de las sesiones de calculo, utilice SQLite, como se sugiere en los requerimientos y utilice [SQLAlchemy](http://www.sqlalchemy.org/) como ORM.
Al empezar el proyecto, decidí utilizar solo la función "eval()" como interprete de los cálculos para concentrarme en la estructura de la api. Por supuesto que es inaceptable utilizar "eval()" en un server con el riesgo de seguridad que implica. Luego de haber terminado con la estructura de la app, escribí un parser utilizando [tdparser](https://github.com/rbarrois/tdparser) con las operaciones: suma, resta, multiplicación, division, potencia y logaritmo natural, respetando la procedencia de operadores y con la posibilidad de usar paréntesis.
Finalmente para testing utilice [pytest](https://pytest-flask.readthedocs.org/) y autopep8 para validar que el codigo cumpla el standard PEP8.

Actualmente este código esta corriendo en Heroku: https://ascentio-test.herokuapp.com/

---

## Como correr el proyecto
Para correr el proyecto es necesario tener instalado:
- [Python 3.4.3 +](https://www.python.org/downloads/release/python-343/)
- [PIP](https://pip.pypa.io/en/stable/)
- [VirtualEnv](https://virtualenv.pypa.io/en/latest/)

Para ejecutar el proyecto:
```
$ git clone https://github.com/matiasbastos/python-restful-calc.git
$ cd python-restful-calc
$ virtualenv-3.4 ./env -p python3.4
$ source ./env/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ python manage.py createdb
$ python manage.py runserver
```

Ahora la api esta corriendo en el puerto 5000.

---

## Endpoints

### Agregar Calculo:
Endpoint para agregar cálculos a la sesión actual. Recibe método POST y requiere del parámetro "input". 

> Importante: El parámetro input tiene que ir urlencoded!  "(2+2)*log10/3" => "(2%2b2)*log10/3"


```
POST /calcs PARAMS input=(2%2b2)*log10/3
```

Respuesta: JSON
```
STATUS 201
{
    "output": 3.07011345732539453
}
```

### Obtener Cálculos De La Session Actual:
Endpoint para obtener los cálculos a la sesión actual. Método GET.
```
GET /calcs 
```

Respuesta: JSON
```
STATUS 200
{
    "current_session_calcs": [
        {
            "input": "(2+2)*log10/3",
            "output": 3.07011345732539453
        }
    ]
}
```

### Guardar Sesión Actual:
Endpoint para guardar la sesión de cálculos actual. Método POST.
```
POST /sessions/nombre_de_la_sesion
```

Respuesta: JSON
```
STATUS 201
{
    "message": "Session saved. id: 1, name: nombre_de_la_sesion"
}
```

### Obtener Sesión:
Endpoint para obtener sesión por su nombre. Método GET.
```
GET /sessions/nombre_de_la_sesion
```

Respuesta: JSON
```
STATUS 200
{
    "session": {
        "id": 1,
        "name": "nombre_de_la_sesion",
        "operations": [
            {
                "id": 1,
                "input": "(2+2)*log10/3",
                "output": "3.0701134573253945"
            }
        ]
    }
}
```

### Obtener Todas Las Sesiones:
Endpoint para obtener todas las sesiones. Método GET.
```
GET /sessions
```

Respuesta: JSON
```
STATUS 200
{
    "sessions": [
        {
            "id": 1,
            "name": "nombre_de_la_sesion",
            "operations": [
                {
                    "id": 1,
                    "input": "(2+2)*log10/3",
                    "output": "3.0701134573253945"
                }
            ]
        }
    ]
}
```

---

### Unit Testing
Para ejecutar los tests, escribir lo siguiente en la terminal:
```
$ py.test tests -v
```

La salida esperada es:

```
========================================================== test session starts ==========================================================
platform darwin -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy-0.3.1 -- /Applications/MAMP/htdocs/ascentio-test/env/bin/python3.4
cachedir: tests/.cache
rootdir: /Applications/MAMP/htdocs/ascentio-test/tests, inifile:
plugins: flask-0.10.0
collected 19 items

tests/test_classes.py::TestClasses::test_parser_sum PASSED
tests/test_classes.py::TestClasses::test_parser_rest PASSED
tests/test_classes.py::TestClasses::test_parser_multiplication PASSED
tests/test_classes.py::TestClasses::test_parser_division PASSED
tests/test_classes.py::TestClasses::test_parser_power PASSED
tests/test_classes.py::TestClasses::test_parser_log PASSED
tests/test_classes.py::TestClasses::test_parser_big_result PASSED
tests/test_classes.py::TestClasses::test_parser_combinated_calc PASSED
tests/test_config.py::TestConfig::test_dev_config PASSED
tests/test_config.py::TestConfig::test_test_config PASSED
tests/test_config.py::TestConfig::test_prod_config PASSED
tests/test_models.py::TestModels::test_session_save PASSED
tests/test_models.py::TestModels::test_operation_save PASSED
tests/test_urls.py::TestUrls::test_add_calc PASSED
tests/test_urls.py::TestUrls::test_get_current_calcs PASSED
tests/test_urls.py::TestUrls::test_get_clean_current_calcs PASSED
tests/test_urls.py::TestUrls::test_save_session PASSED
tests/test_urls.py::TestUrls::test_get_session PASSED
tests/test_urls.py::TestUrls::test_get_sessions PASSED

======================================================= 19 passed in 0.72 seconds =======================================================
```

---

## Ideas
Algunas mejoras o características que me gustaría agregar:
- Continuous integration.
- Documentación.
- Cliente Web para la api.
- Agregar mas operaciones de calculo y constantes.
- Mejorar control de errores.


## Autor

[Matias Bastos](https://ar.linkedin.com/in/matiasbastos)
