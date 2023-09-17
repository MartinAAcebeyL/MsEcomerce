import os
import grpc

from google.cloud import firestore
from google.cloud.firestore_v1.base_client import BaseClient

# Función para crear una conexión a Firestore.

# Si están definidas la variables de entorno FIRESTORE_EMULATOR_HOST
# y FIRESTORE_PROJECT_ID, entonces tratará de conectarse con el emulador
# con una colección simulada; si sólo viene la variable FIRESTORE_PROJECT_ID,
# entonces se conectará al Firestore de GCP especificado ahí, y si no vienen
# ninguna de las dos variables entonces se conecta al Firestore especificado
# en la configuración local del GCloud SDK.

def create_firestore_client():
    
    project_id = os.environ.get("FIRESTORE_PROJECT_ID")

    monkey_patch_firestore_emulator()
    return firestore.Client(project = project_id)

def monkey_patch_firestore_emulator():

    # Parche para habilitar la conexión al emulador de Firestore
    # si es que se encuentra en otro contenedor. Se debe llamar
    # antes de crear el cliente.

    # Obtenido de https://github.com/googleapis/python-firestore/issues/335

    def _emulator_channel(self, transport):
        if "GrpcAsyncIOTransport" in str(transport.__name__):
            return grpc.aio.insecure_channel(self._emulator_host)
        else:
            return grpc.insecure_channel(self._emulator_host)

    BaseClient._emulator_channel = _emulator_channel