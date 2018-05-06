from flask import Flask, Response, request
from flask_rrbac import RoleRouteBasedACL
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import current_user


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_app_1.db'
app.config['SECRET_KEY'] = 'sqlite:///test_app_1.db'
app.config['RRBAC_ANONYMOUS_ROLE'] = 'Anon'
app.config['DEBUG'] = True
app.config['TESTING'] = True

rrbac = RoleRouteBasedACL(
    app,
    user_loader=lambda: current_user
)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/uncovered_route')
@rrbac._authenticate
def uncovered_route():
    return Response('uncovered_route')


@app.route('/covered_route', methods=['GET', 'POST'])
@rrbac._authenticate
def covered_route():
    return Response('covered_route')


@app.route('/covered_route/<int>', methods=['GET', 'POST'])
@rrbac._authenticate
def number_covered_route():
    return Response('{}'.format(request.method))


def tear_down():
    db.session.close()
    db.drop_all()