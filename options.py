
import configparser

#Get directory from config.ini
def opt_dir():
    #global path
    config = configparser.RawConfigParser()
    config.read_file(open('config.ini'))
    if config.get('SETTINGS', 'dir', raw=True) == "":
        return "ERROR DIR NOT MENTIONED"
    else:
        path = config.get('SETTINGS', 'dir', raw=True)
        return path
