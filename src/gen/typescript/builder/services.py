from config.Service import Service
from util.writer import *
from reader.Table import Field

def generateBodyValidate(field:Field):
    body = f"        await body('{field.getName()}')"
    if field.getType() == 'numeric':
        body += ".isNumeric().run(req)\n"
    else:
        body += ".isString().trim().run(req)\n"
    return body


def generateListFunction(service:Service, file:str):
    
    listTemplate = read(file)
    table = service.getTable()
    fields = table.getNotChangeFields()

    bodyStr  = ""
    fieldstr = "" 
    for field in fields:
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    listTemplate = listTemplate.replace("[#fields]", fieldstr[:-1])
    listTemplate = listTemplate.replace("[#body_validate]", bodyStr)
    listTemplate = listTemplate.replace("[#service]", service.getName())

    return listTemplate


def generateCreateFunction(service:Service,file:str):

    createTemplate = read(file)
    table = service.getTable()

    bodyStr  = ""
    fieldstr = "" 
    paramsInserted = []

    for field in table.getFields(primary=False):
        paramsInserted.append(field.getName())
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    for field in table.getNotChangeFields():
        if field.getName() in paramsInserted: 
            continue
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    createTemplate = createTemplate.replace("[#fields]", fieldstr[:-1])
    createTemplate = createTemplate.replace("[#body_validate]", bodyStr)
    createTemplate = createTemplate.replace("[#service]", service.getName())

    return createTemplate



def generateDeleteFunction(service:Service, file:str):
    
    deleteTemplate = read(file)
    table = service.getTable()
    fieldPrim = table.getPrimaryKey()
    fields = table.getNotChangeFields()

    bodyStr  = ""
    fieldstr = "" 
    for field in fields:
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    fieldstr += fieldPrim.getName()+","
    bodyStr  += generateBodyValidate(field=fieldPrim)

    deleteTemplate = deleteTemplate.replace("[#fields]", fieldstr[:-1])
    deleteTemplate = deleteTemplate.replace("[#body_validate]", bodyStr)
    deleteTemplate = deleteTemplate.replace("[#service]", service.getName())

    return deleteTemplate


def generateUpdateFunction(service:Service,file:str):

    updateTemplate = read(file)
    table = service.getTable()
    fieldPrim = table.getPrimaryKey()

    bodyStr  = ""
    fieldstr = "" 
    paramsInserted = []

    for field in table.getFields(primary=False):
        paramsInserted.append(field.getName())
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    for field in table.getNotChangeFields():
        if field.getName() in paramsInserted: 
            continue
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    fieldstr += fieldPrim.getName()+","
    bodyStr  += generateBodyValidate(field=fieldPrim)

    updateTemplate = updateTemplate.replace("[#fields]", fieldstr[:-1])
    updateTemplate = updateTemplate.replace("[#body_validate]", bodyStr)
    updateTemplate = updateTemplate.replace("[#service]", service.getName())

    return updateTemplate


def generateUniqueFunction(service:Service, file:str):
    
    uniqueTemplate = read(file)
    table = service.getTable()
    fieldPrim = table.getPrimaryKey()

    bodyStr  = ""
    fieldstr = "" 

    for field in table.getNotChangeFields():
        fieldstr += field.getName()+","
        bodyStr  += generateBodyValidate(field=field)

    fieldstr += fieldPrim.getName()+","
    bodyStr  += generateBodyValidate(field=fieldPrim)

    uniqueTemplate = uniqueTemplate.replace("[#fields]", fieldstr[:-1])
    uniqueTemplate = uniqueTemplate.replace("[#body_validate]", bodyStr)
    uniqueTemplate = uniqueTemplate.replace("[#service]", service.getName())

    return uniqueTemplate


def generateFunctionService(service:Service, route_templates:str):

    functions = service.getApiFunctions()
    functionsTemplate = ""

    for func in functions:
        if func.getFuncName() == 'list':
            functionsTemplate += generateListFunction(service, route_templates+'/services/templates/list.template.txt')+","
        elif func.getFuncName() == 'create':
            functionsTemplate += generateCreateFunction(service, route_templates+'/services/templates/create.template.txt')+","
        elif func.getFuncName() == 'delete':
            functionsTemplate += generateDeleteFunction(service, route_templates+'/services/templates/delete.template.txt')+","
        elif func.getFuncName() == 'update':
            functionsTemplate += generateUpdateFunction(service, route_templates+'/services/templates/update.template.txt')+","
        elif func.getFuncName() == 'unique':
            functionsTemplate += generateUniqueFunction(service, route_templates+'/services/templates/unique.template.txt')+","

    return functionsTemplate