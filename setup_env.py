from db import Sensors, Devices

if __name__ == '__main__':
    Sensors.create_table()
    Devices.create_table()