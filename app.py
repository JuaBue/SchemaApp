# app.py
import flask
from flask import request
from flask_cors import CORS
from flask_restplus import Api, Resource, Namespace, fields
from database import BaseDB
import os


# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = flask.Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='IOON', description='Backend description for the web application IOON')
app.secret_key = os.urandom(24)
app.config['CORS_HEADERS'] = 'Content-Type'


namespace_user = Namespace("test", description='Methods for test')
api.add_namespace(namespace_user)

request_fields = api.model('Test', {
    'data': fields.Integer
})

@namespace_user.route('/index')
class Test(Resource):
    @api.response(404, 'BAD_REQUEST')
    @api.response(200, 'OK')
    @api.doc(body=request_fields)
    def post(self):
        body = request.json
        handler = BaseDB()
        try:
            handler.engine.execute(handler.table.insert(), dato1=body['data'])
        except Exception as Error:
            return {'message': str(Error)}, 404
        return {'message': 'Dato insertado correctamente [%d].' % (body['data'])}, 200

    @api.response(200, 'OK')
    def get(self):
        handler = BaseDB()
        data = handler.getdata()
        return {'message': 'Acceso a los datos correcto', 'datos': data}, 200


    @api.response(200, 'OK')
    def delete(self):
        handler = BaseDB()
        if handler.erasedata():
            return {'message': 'Datos borrados correctamente'}, 200
        else:
            return {'message': 'Error al borrar los datos'}, 404

@namespace_user.route('/initdb')
class Init(Resource):
    @api.response(200, 'OK')
    def get(self):
        handler = BaseDB()
        try:
            handler.engine.execute(handler.table.insert(), dato1=12)
        except Exception as Error:
            return {'message': str(Error)}, 400
        return {'message': 'Base de datos inicializada correctamente.'}, 200





if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
