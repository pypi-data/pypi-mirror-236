import time
from octasonic import Octasonic

octasonic = Octasonic(0)
protocol_version = octasonic.get_protocol_version()
firmware_version = octasonic.get_firmware_version()
print("Protocol v%s; Firmware v%s" % (protocol_version, firmware_version))
octasonic.set_sensor_count(8)
print("Sensor count: %s" % octasonic.get_sensor_count())
while True:
    octasonic.toggle_led()
    time.sleep(0.25)
    readings = []
    for i in range(0, 7):
        readings.append(octasonic.get_sensor_reading(i))
    print(readings)
