from peewee import *
from playhouse.cockroachdb import JSONField

from config import BaseModel


class User(BaseModel):
    user_id = AutoField()
    username = CharField()
    email = CharField()
    password = CharField()
    confirmed = BooleanField(default=False)


def get_users():
    for user in User.select():
        if user.confirmed:
            print(user.username, "\tconfirmed")
        else:
            print(user.username, "\tunconfirmed")


def create_user(username, email, password):
    fuck = User.select().count()
    User.create(user_id=fuck, username=username, email=email, password=password)


def check_user_data_collision(username, email):
    try:
        return User.select().where(((User.username == username) | (User.email == email)) & User.confirmed)
    except DoesNotExist:
        return 0


def check_user(login, password):
    try:
        return User.get(User.username == login, User.password == password, User.confirmed).user_id
    except DoesNotExist:
        pass
    try:
        return User.get(User.email == login, User.password == password, User.confirmed).user_id
    except DoesNotExist:
        pass
    return -1


def get_username_by_id(user_id):
    try:
        return User.get_by_id(user_id).username
    except DoesNotExist:
        return 'error'


def get_mail_by_username(username):
    try:
        return User.get(User.username == username).email
    except DoesNotExist:
        return 'error'


def confirm_user(username):
    try:
        return User.update(confirmed=True).where(User.username == username).execute()
    except DoesNotExist:
        return 'error'


class Sensors(BaseModel):
    serial_number = CharField()
    type_int = IntegerField()
    type_hr = CharField()


class Devices(BaseModel):
    owner = ForeignKeyField(User, related_name='device')
    serial_number = CharField()
    hr_name = CharField(null=True)


#
# class Logic(BaseModel):
#     output_id = IntegerField()
#     logic = JSONField()


if __name__ == '__main__':
    if Sensors.select().where(Sensors.serial_number == 'test_field').exists():
        print('zbc')
