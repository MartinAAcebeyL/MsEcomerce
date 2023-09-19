from datetime import datetime, timezone
import jwt
from functools import wraps
from flask import request, jsonify

# Funciones de utilidad para el sistema completo.

# Si bien no va dentro de ninguna de las carpetas de contexto ("books" o "greeting"),
# estas funciones corresponden a la capa más interna de Clean Architecture, que corresponde
# a la capa Entities. Esta capa no solamente puede contener entidades, sino cualquier código
# que es usado a nivel de aplicación completo.

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def jwt_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if token and token.startswith('Bearer '):
                token = token.split(' ')[1]

                try:
                    payload = jwt.decode(
                        token, 'SECRET_KEY', algorithms=['HS256'])
                    is_admin = payload.get('is_admin')

                    # Verifica si se requiere un rol específico (si se proporciona)
                    if roles is None or (is_admin and 'admin' in roles):
                        return f(*args, **kwargs)
                    else:
                        # Código 403 para acceso no autorizado
                        return jsonify({'message': 'Permiso denegado'}), 403
                except jwt.ExpiredSignatureError:
                    # Código 401 para token expirado
                    return jsonify({'message': 'Token expirado'}), 401
                except jwt.DecodeError:
                    # Código 401 para token inválido
                    return jsonify({'message': 'Token inválido'}), 401
            else:
                # Código 401 para falta de token
                return jsonify({'message': 'Token de acceso requerido'}), 401
        return decorated_function
    return decorator


def filter_dict(dict, fields):

    # Filtra el diccionario entrante, retornando nuevo diccionario
    # sólo con los campos definidos y descartando los demás.

    filtered_dict = {}

    for key in dict:

        if key in fields:
            filtered_dict[key] = dict[key]

    return filtered_dict


def format_date(datetime):

    # Retorna una representación en String de una fecha/hora dada.

    return datetime.strftime(DATE_FORMAT)


def get_current_datetime():

    # Retorna la fecha actual en UTC-0

    return datetime.now(timezone.utc)
