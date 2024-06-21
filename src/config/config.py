from util import mysqli
import json
from config.Config import *

def config():
    with open('./config.json', 'r') as file:
        data = json.load(file)
        return Config(data)