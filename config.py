from peewee import SqliteDatabase, Model

HTTP_PORT = 5002
HOST = '0.0.0.0'
CREDENTIAL_KEY = "fuckit"  # TODO: replace with some rng algoritm
NOT_NEED_AUTH = 1
LIGHT_NORMAL = 150

sensor_type = {1: 'button', 2: 'light', 3: 'temperature'}


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('SoftHouse.db')
