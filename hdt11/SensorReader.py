import Adafruit_DHT
import time
import logging

from datetime import datetime

class SensorReader(object):
    
    log = logging.getLogger("SensorReader")

    def __init__(self, dht_type, dhtp_pin):
        self.dht_type = dht_type
        self.dht_pin = dhtp_pin
        
    def read_sensor(self):
        humidity, temp = Adafruit_DHT.read(self.dht_type, self.dht_pin)
        if humidity is None or temp is None:
            time.sleep(2)
            self.log.warning('... Read new values ...')
            return self.read_sensor()
        self._log_temp_and_hum(temp, humidity)
        return humidity, temp

    def _log_temp_and_hum(self, temperature, humidity):
        self.log.info('{0} T: {1:3} C, H:{2:3} %'.format(datetime.now().time(),temperature,humidity))
