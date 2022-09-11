
import configparser

#Get directory from config.ini
def opt_dir():
    #global path
    config_file = configparser.RawConfigParser()
    config_file.read_file(open('settings.ini'))
    if config_file.get('SETTINGS', 'dir', raw=True) == "":
        return "ERROR DIR NOT MENTIONED"
    else:
        path = config_file.get('SETTINGS', 'dir', raw=True)
        return path
