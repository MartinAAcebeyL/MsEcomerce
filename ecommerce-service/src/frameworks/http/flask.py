from enviame.inputvalidation import flask_error_handler

from flask import Flask
    
def create_flask_app(blueprints):

    # Función para crear una aplicación de Flask con todos sus blueprints (endpoints) asociados.
    # Asocia además el manejador de errores encontrado en la librería de validaciones.
    
    app = Flask(__name__)

    app.register_error_handler(Exception, flask_error_handler)
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)



    return app
