import configparser
import json



name = 'b_bot'
version = '0.2.1'
reposting = False

access_token = ''
app_id = '5468754'
my_id = ''
api_version = '5.64'

config_path = "b_bot.config"
token_path = "token.st"


def copy_default_config():
    config_file = open(config_path, 'w')
    default_config = open("b_bot.config.default", 'r')
    config_file.write(default_config.read())
    config_file.close()
    default_config.close()
    
##Checking files for existence
#configuration file
try:
    open(config_path).close()
except IOError:
    copy_default_config()
#token file
try:
    open(token_path).close()
except IOError:
    open(token_path, 'w').close()



config = configparser.ConfigParser()
config.read(config_path)

try:
    reposting = config.getboolean("settings", "reposting")
except ValueError:
    print('Не удалось найти ' + config_path)
except configparser.NoSectionError:
    copy_default_config()

with open(token_path, "r") as token_file:
    access_token = token_file.read()
    ##my_id = config.get("private", "my_id")

def save_token(token):
    with open(token_path, 'w') as token_file:
        token_file.write(token)
