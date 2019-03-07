# Initializes a Python module


#import os  # (from pocoo tutorial)

from flask import Flask
app = Flask(__name__, instance_relative_config=True)


from app import views
app.config.from_object('config')




# FROM POCOO (finishing scotch tutorial then will think about function instead)
'''
def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
'''

# NOTES:
#
# http://flask.pocoo.org/docs/1.0/tutorial/factory/
# Suggests having FUNCTION instead of global app declaration
# Commands to run (BASH):
# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run
#
# https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework
# Recommended directory structure:
# |-- my-project
#     |-- app
#     |   |-- __init__.py
#     |   |-- templates
#     |   |-- views.py
#     |-- instance (should not be pushed to version control, e.g. passwords / keys)
#         |-- config.py
#     |-- run.py
#     |-- config.py
#     |-- requirements.txt
# Commands to run (BASH):
# export FLASK_APP=run.py
# flask run
