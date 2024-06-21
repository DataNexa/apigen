from typing import Union, List
from reader.Table import Table

class MiddlewareService:

    _slug:str = ''
    _inject:List[str]

    def __init__(self, dataMid):

        self._slug   = dataMid['slug']

        if 'inject' in dataMid:
            self._inject = dataMid['inject']

    def getSlug(self):
        return self._slug
    
    def getInject(self):
        return self._inject

    def toString(self):
        string  = "        _slug: "+self._slug+" \n"
        string += "        _inject: "+str(self._inject)+" \n"
        return string


class APIfunction:

    _func:str
    _middlewares:List[MiddlewareService]

    def __init__(self, dataApiFunction):

        self._func = dataApiFunction['func']
        self._middlewares = []
        for mid in dataApiFunction['middlewares']:
            self._middlewares.append(MiddlewareService(mid))

    def getFuncName(self):
        return self._func

    def getMiddlewares(self):
        return self._middlewares

    def toString(self):
        string  = "-------------------"+" \n"
        string += "_func: "+self._func+" \n"
        string += "_middlewares:  \n"
        for mid in self._middlewares:
            string += mid.toString()+"\n"
        return string


class Service:
    
    _name:str
    _tableName:str
    _table:Table
    _ignore_functions:List[str]
    _api_functions:List[APIfunction]
    _required_fields_to_list:List[str]
    _required_fields_to_create:List[str]
    _tree:List[str]

    _querys_adhoc:dict[str,str]

    def __init__(self, serviceData):
        
        self._name          = serviceData['name']
        self._tableName     = serviceData['table']
        self._api_functions = [] 
        self._querys_adhoc  = {}
        
        if 'ignore_functions' in serviceData:
            self._ignore_functions = serviceData['ignore_functions']

        if 'api_functions' in serviceData:
            for api_func in serviceData['api_functions']:
                self._api_functions.append(APIfunction(api_func))

        if 'tree' in serviceData:
            self._tree = serviceData['tree']


    def setQueryAdhoc(self, key, value):
        self._querys_adhoc[key] = value

    def getQueryAdhoc(self, key):
        return self._querys_adhoc[key]

    def getName(self):
        return self._name

    def setTable(self, table:Table):
        self._table = table

    def getTable(self):
        return self._table

    def getTableName(self):
        return self._tableName

    def getApiFunctions(self):
        return self._api_functions

    def getIgnoreFunctions(self):
        return self._ignore_functions

    def getTree(self):
        return self._tree

    def toString(self):
        string  = ""
        string += "-------------------"+" \n"
        string += "   _name: "+self._name +" \n"
        string += "   _table: "+self._table +" \n"
        string += "   _ignore_functions: "+str(self._ignore_functions)+" \n"
        string += "   _required_fields_to_list: "+str(self._required_fields_to_list)+" \n"
        string += "   _required_fields_to_create: "+str(self._required_fields_to_create)+" \n"
        string += "   _tree: "+str(self._tree)+" \n"
        for api in self._api_functions:
            string += "        "+ api.toString()+" \n"
        return string