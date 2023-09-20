# Prueba tecnica de Enviame

### Descripcion

Test tecnico sobre la construccion de un microservicio de un E-comerce

## Requisitos

- Docker installed
- Python 3.7

## Instalacion y ejecucion

- Clona el proyecto.

- Construir los contenedores: `docker-compose up --build`

Una vez creado los contenedores y la base de datos con las tablas(quiza debe reiniciar los servicios para que esto suceda), podemos pasar a crear datos de prueba:

1. Debemos entrar al servicio de la app con: `docker-compose exec ecommerce-app bash`
2. Exporta la Ruta del Proyecto al PYTHONPATH: `export PYTHONPATH=/app:$PYTHONPATH`
3. Correr el script: `python src/create_fake_data.py` Y se crearan datos de prueba.

Se agrego las colecciones postman [aqui](./Colleciones%20de%20postman/)

De forma predeterminada, los microservicios se ejecutarán en los siguientes puertos:

- ecommerce-service: 8000
