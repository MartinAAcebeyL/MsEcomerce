from flask import Blueprint

# Endpoints para la sección de saludos.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

def create_greeting_blueprint(greeting_usecase):

    blueprint = Blueprint("greeting", __name__)

    @blueprint.route("/greeting")
    def make_greeting():        
        return greeting_usecase.make_greeting()

    return blueprint