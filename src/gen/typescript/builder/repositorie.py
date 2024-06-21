from config.Service import Service
from reader.Table import Table
from util.writer import *

def generateUniqueFunction(service:Service, file:str):

    uniqueTemplate = read(file)

    table = service.getTable()
    params = ""
    values = ""

    uniqueTemplate = uniqueTemplate.replace("[#service]", service.getName())
    qadhoclist = service.getQueryAdhoc('list')
    andcond = False

    for field in table.getNotChangeFields():
        andcond = True
        param   = field.getName()+":"
        values += field.getName()+","
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    field   = table.getPrimaryKey()
    param   = field.getName()+":"
    values += field.getName()+","
    if(field.getType() == 'numeric'):
        param += "number"
    else:
        param += "string"
    params += param+","

    condti = "        and " if andcond else "      where "
    qadhoclist += condti+table.getName()+"."+field.getName()+" = ? "
    uniqueTemplate = uniqueTemplate.replace("[#query_list]", qadhoclist)

    uniqueTemplate = uniqueTemplate.replace("[#params]", params[:-1])
    uniqueTemplate = uniqueTemplate.replace("[#values]", values[:-1])

    return uniqueTemplate

def generateDeleteFunction(service:Service, file:str):
    
    deleteTemplate = read(file)
    table = service.getTable()
    params = ""
    values = ""

    deleteTemplate = deleteTemplate.replace("[#service]", service.getName())
    deleteTemplate = deleteTemplate.replace("[#query_delete]", service.getQueryAdhoc('delete'))

    for field in table.getNotChangeFields():
        param   = field.getName()+":"
        values += field.getName()+","
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    field = table.getPrimaryKey()
    param   = field.getName()+":"
    values += field.getName()+","
    if(field.getType() == 'numeric'):
        param += "number"
    else:
        param += "string"
    params += param+","

    deleteTemplate = deleteTemplate.replace("[#params]", params[:-1])
    deleteTemplate = deleteTemplate.replace("[#values]", values[:-1])
    
    return deleteTemplate

def generateUpdateFunction(service:Service, file:str):

    updateTemplate = read(file)
    table = service.getTable()
    params = ""
    values = ""

    paramsInserted = []

    for field in table.getFields(primary=False):
        paramsInserted.append(field.getName())
        param   = field.getName()+":"
        values += field.getName()+","
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    for field in table.getNotChangeFields():
        values += field.getName()+","
        if field.getName() in paramsInserted: 
            continue
        param   = field.getName()+":"
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    field = table.getPrimaryKey()
    param   = field.getName()+":"
    values += field.getName()+","
    if(field.getType() == 'numeric'):
        param += "number"
    else:
        param += "string"
    params += param+","
    
    updateTemplate = updateTemplate.replace("[#query_update]", service.getQueryAdhoc('update'))
    updateTemplate = updateTemplate.replace("[#params]", params[:-1])
    updateTemplate = updateTemplate.replace("[#values]", values[:-1])
    
    return updateTemplate


def generateCreateFunction(service:Service, file:str):
    
    createTemplate = read(file)
    table = service.getTable()
    params = ""
    values = ""

    createTemplate = createTemplate.replace("[#service]", service.getName())
    paramsInserted = []

    for field in table.getFields(primary=False):
        paramsInserted.append(field.getName())
        param   = field.getName()+":"
        values += field.getName()+","
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    for field in table.getNotChangeFields():
        values += field.getName()+","
        if field.getName() in paramsInserted: 
            continue
        param   = field.getName()+":"
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    createTemplate = createTemplate.replace("[#query_create]", service.getQueryAdhoc('create'))
    createTemplate = createTemplate.replace("[#params]", params[:-1])
    createTemplate = createTemplate.replace("[#values]", values[:-1])
    
    return createTemplate


def generateListFunction(service:Service, file:str):
    
    listTemplate = read(file)
    table = service.getTable()
    params = ""
    values = ""

    listTemplate = listTemplate.replace("[#service]", service.getName())
    listTemplate = listTemplate.replace("[#query_list]", service.getQueryAdhoc('list'))

    for field in table.getNotChangeFields():
        param   = field.getName()+":"
        values += field.getName()+","
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+","

    listTemplate = listTemplate.replace("[#params]", params)
    listTemplate = listTemplate.replace("[#values]", values[:-1])

    return listTemplate


def generateFunctionsRepository(service:Service, route_templates:str):
    
    functions = service.getApiFunctions()
    functionsTemplate = ""

    for func in functions:
        if func.getFuncName() == 'list':
            functionsTemplate += generateListFunction(service, route_templates+'/repositories/templates/list.template.txt')+","
        elif func.getFuncName() == 'create':
            functionsTemplate += generateCreateFunction(service, route_templates+'/repositories/templates/create.template.txt')+","
        elif func.getFuncName() == 'delete':
            functionsTemplate += generateDeleteFunction(service, route_templates+'/repositories/templates/delete.template.txt')+","
        elif func.getFuncName() == 'update':
            functionsTemplate += generateUpdateFunction(service, route_templates+'/repositories/templates/update.template.txt')+","
        elif func.getFuncName() == 'unique':
            functionsTemplate += generateUniqueFunction(service, route_templates+'/repositories/templates/unique.template.txt')+","

    return functionsTemplate[:-1]