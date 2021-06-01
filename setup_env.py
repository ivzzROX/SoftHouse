from db import Sensors, Devices, User, Logic

if __name__ == '__main__':
    Sensors.create_table()
    User.create_table()
    Devices.create_table()
    Logic.create_table()

