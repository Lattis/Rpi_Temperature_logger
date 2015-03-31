import ConfigParser
import logging

class Config(object):
    
    log = logging.getLogger("Config")
    
    def __init__(self, file="TempLogger.cfg"):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(file)
        self.dump_cfg()
        
    def dump_cfg(self):
        self.log.debug("Found Sections in config : {0}".format(self.config.sections()))
        
    def get_email(self):
        return self.config.get("GDocs", "email")
    
    def get_api_key(self):
        return self.config.get("GDocs", "api_key")
    
    def get_worksheet_name(self):
        return self.config.get("GDocs", "worksheet_name")
    
    def get_dht_pin(self):
        return self.config.getint("DHT", "pin")
    
    def get_dht_type(self):
        return self.config.getint("DHT", "type")
    
    def get_measure_interval(self):
        return self.config.getint("Logger", "measure_interval")
    
    def get_log_avg_interval(self):
        return self.config.getint("Logger", "log_avg_interval")