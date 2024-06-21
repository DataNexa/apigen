from config.Service import Service
from typing import List, Dict, Any
from util.MySQLi import MySQLi

class Middleware:

    _import:str
    _value:str

    def __init__(self, dataFile):
        self._import = dataFile['import']
        self._value = dataFile['value']

    def getImport(self):
        return self._import 
    
    def getValue(self):
        return self._value


class Config:

    _error   = False
    _message = ''

    _database = {
        "user":"",
        "pass":"",
        "host":"",
        "name":""
    }
    
    _services:List[Service] = []
    _middlewares:Dict[str, Middleware] = {}

    def __init__(self, config):
        
        if 'database' not in config:
            self._message = 'Não há um banco configurado'
            self._error = True
            return 
            
        database = config['database']

        if not {'user', 'pass', 'host', 'name'}.issubset(database.keys()):
            self._message = "banco de dados foi configurado faltando um ou mais atributos de : { 'user', 'password', 'host', 'db' }"
            self._error = True
            return 

        MySQLi(
            host=database['host'], 
            user=database['user'], 
            password=database['pass'], 
            database=database['name']
        )

        self._database["user"] = database["user"]
        self._database["pass"] = database["pass"]
        self._database["host"] = database["host"]
        self._database["name"] = database["name"]

        if 'middlewares' in config:
            for key in config['middlewares'].keys():
                self._middlewares[key] = Middleware(config['middlewares'][key])

        if 'services' in config and isinstance(config['services'], list):
            for serv in config['services']:
                servo = Service(serv)
                self._services.append(servo)


    def getServices(self):
        return self._services

    def getMiddlewares(self):
        return self._middlewares

    def toString(self):
        string  = 'Conf: \n'
        string += '----- database: \n'
        string += '----- '+str(self._database)+"\n"
        string += '----- services:'+" \n"
        for serv in self._services:
            string += "     "+serv.toString()+" \n"

        return string