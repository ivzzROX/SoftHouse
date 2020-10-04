from peewee import *

from config import BaseModel


class Sensors(BaseModel):
    serial_number = CharField()
    type_int = IntegerField()
    type_hr = CharField()


if __name__ =='__main__':
    if Sensors.select().where(Sensors.serial_number == 'test_field').exists():

        print('zbc')

