import configparser

config = configparser.ConfigParser()
config.read('config.ini')

server = config['login_credentials']['server']
database = config['login_credentials']['database']
username = config['login_credentials']['username']
password = config['login_credentials']['password']