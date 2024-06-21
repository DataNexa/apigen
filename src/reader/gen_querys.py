from config.Service import Service, APIfunction
from util.mysqli import *
from reader.Table import Table

def createTable(tablename:str, trees:[str]):

    res = query('desc '+tablename)
    join = ''
    whereJoin = ''
    not_change_fields = []

    if len(trees) > 0:

        whereJoin += ' WHERE '

        foreign = query(f"""
            SELECT
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
                TABLE_NAME = '{tablename}' AND
                CONSTRAINT_NAME <> 'PRIMARY';
        """)
        
        foreing_table   = foreign[0][1]
        column          = tablename+"."+foreign[0][0] 
        reference       = f"{foreing_table}.{foreign[0][2]}"

        not_change_fields.append(foreign[0][0])

        join += f"     join {foreing_table} on {column} = {reference} \n"
        whereJoin += f" {reference} = ? and "

        for tree in trees:
            foreign = query(f"""
                SELECT
                    COLUMN_NAME,
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE
                    TABLE_NAME = '{tree}' AND
                    CONSTRAINT_NAME <> 'PRIMARY';
            """)

            if foreign[0][1] is None:
                continue

            foreing_table   = foreign[0][1]
            column          = tree+"."+foreign[0][0]
            reference       = f"{foreing_table}.{foreign[0][2]}"

            not_change_fields.append(foreign[0][0])

            join += f"         join {foreing_table} on {column} = {reference} \n"
            whereJoin += f" {reference} = ? and "
            
    if whereJoin != '':
        whereJoin = whereJoin[:-4]
    
    table = Table(tablename, res, join, whereJoin)
    table.setNotChangeFieldNames(not_change_fields)

    return table


def genQueryList(table:Table):
    return f""" 
        SELECT {table.getFieldsName()}
        from {table.getName()} 
        {table.getJoin()} 
        {table.getWhereJoin()}
    """

def genQueryCreate(table:Table):
    return f"""
        insert into {table.getName()}({table.getFieldsName(False, True)}) 
        VALUES ({(('?,') * table.countFields(True))[:-1]})
        {table.getJoin()}
        {table.getWhereJoin()}
    """

def genQueryUpdate(table:Table):

    updateString = f"update {table.getName()} set "
    fields = table.getUpdatableFields()
    for field in fields:
        updateString += f" {field.getName()} = ?, "

    updateString  = updateString[:-2]
    updateString += table.getJoin()
    updateString += "        "+table.getWhereJoin()

    primary = table.getPrimaryKey()

    if primary is not None:
        updateString += f" and {table.getName()}.{primary.getName()} = ? "

    return updateString

def genQueryDelete(table:Table):
    
    delteString = f"\n         delete from {table.getName()} \n     {table.getJoin()} \n       {table.getWhereJoin()} "

    primary = table.getPrimaryKey()

    if primary is not None:
        delteString += f" and {table.getName()}.{primary.getName()} = ? "

    return delteString

def genQuerySearch():
    pass

def gen_querys(service:Service):
    
    table = createTable(service.getTableName(), service.getTree())
    
    functions = service.getApiFunctions()

    for func in functions:
        name  = func.getFuncName()
        query = ""
        if  name  == 'list':
            query = genQueryList(table)
        elif name == 'create':
            query = genQueryCreate(table)
        elif name == 'update':
            query = genQueryUpdate(table)
        elif name == 'delete':
            query = genQueryDelete(table)
            
        else:
            name = ""
        service.setQueryAdhoc(name, query)
        service.setTable(table)
    