import logging as log
import time
from GDocs import GDocs
from Config import Config
from hdt11.SensorReader import SensorReader


def get_avg(values):
    return reduce(lambda x, y: x + y, values) / len(values)

def collect_values(log_avg_interval, measure_interval, reader):
    hum_list = []
    temp_list = []
    for i in range(0, log_avg_interval):
        humidity, temp = reader.read_sensor()
        if humidity is not None:
            hum_list.append(humidity)
        if temp is not None:
            temp_list.append(temp)
        time.sleep(measure_interval)
        
    return hum_list, temp_list

if __name__ == '__main__':
    # Init logger 
    log.basicConfig(filename='/home/pi/TemperatureLog.log', level=log.ERROR, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    config = Config.Config()
    
    gdocs = GDocs.GDocs(config.get_email(), config.get_api_key())
    gdocs.initialize()
    
    reader = SensorReader(config.get_dht_type(), config.get_dht_pin())
    try:
        row = 2
        log_avg_interval = config.get_log_avg_interval()
        measure_interval = config.get_measure_interval()
        while True:
            log.info("Start collecting values ...")
            hum_list, temp_list = collect_values(log_avg_interval, measure_interval, reader)
            avg_humidity = get_avg(hum_list)
            avg_temperature = get_avg(temp_list)
            log.info("Collected average values : Temperature : {1:2}; Humidity : {0:2}".format(avg_humidity, avg_temperature))
            try:
                gdocs.open_spreadsheet(config.get_worksheet_name())
                gdocs.write_value(1, row, time.asctime())
                gdocs.write_value(2, row, avg_temperature)
                gdocs.write_value(3, row, avg_humidity)
                row += 1
            except Exception as e:
                log.error("Values were not written !", e)
            
    except KeyboardInterrupt as e:
        log.warn(str(e))
    
    pass
