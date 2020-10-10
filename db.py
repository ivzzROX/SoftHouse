from peewee import *
from playhouse.cockroachdb import JSONField

from config import BaseModel


class Sensors(BaseModel):
    serial_number = CharField()
    type_int = IntegerField()
    type_hr = CharField()


class Devices(BaseModel):
    serial_number = CharField()
    hr_name = CharField(null=True)

#
# class Logic(BaseModel):
#     output_id = IntegerField()
#     logic = JSONField()


if __name__ =='__main__':
    if Sensors.select().where(Sensors.serial_number == 'test_field').exists():

        print('zbc')

