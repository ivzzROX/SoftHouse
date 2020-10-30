from db import Sensors, Devices, User

if __name__ == '__main__':
    Sensors.create_table()
    Devices.create_table()
    User.create_table()

