import configparser


class ConfProperties(object):
    def __init__(self):
        self.__config_properties = configparser.RawConfigParser()
        self.__config_properties.read('application.properties')

    def get_url(self) -> str:
        return self.__config_properties['gpw']['url']


conf_properties = ConfProperties()
