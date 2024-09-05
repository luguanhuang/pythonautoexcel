#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import yaml
import os

class YamlConfig:
    """A class that Parses the yaml style configuration file of user app.
    
    usage:
       file = './config.yaml'
       configs = YamlConfig(file)
           file --> config file name 
       configs.exist_config_option('config', 'description')
           examine if this configuration exists
       configs.get_option_config('config', 'description')
           get Specific configuration
       configs.get_configs()
           get all configurations from config file
   
    """

    def __init__(self, filename):
        self.configs = None

        with open(filename, "r") as f:
            # self.configs = yaml.load(f,Loader=yaml.FullLoader)
            self.configs = yaml.load(f,yaml.Loader)

    def exist_config_option(self, section, option):
        state = False
        if self.configs and section in self.configs and option in self.configs[section]:
            state = True
        return state

    def get_option_config(self, section, option):
        if self.exist_config_option(section, option):
            return self.configs[section][option]
        else:
            return None

    def convert_config_to_integer(self, section, option):
        if self.exist_config_option(section, option):
            try:
                return int(self.configs[section][option])
            except Exception as error:
                print("can not convert config %s to integer. Error:%s" % (self.configs[section][option], error))

    def get_configs(self):
        return self.configs


current_path = os.getcwd()
# print("current_path=", current_path+".\config.yaml")
config_instance = YamlConfig(current_path+".\config.yaml")
config = config_instance.get_configs()

