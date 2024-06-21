import re

def _typed(tipo):
    if tipo == 'date' or tipo == 'datetime':
        return tipo

    tiporeg = re.sub("\(\d+\)", '', tipo)
    numeric_types = ['bigint', 'tinyint', 'int']

    if tiporeg in numeric_types:
        return 'numeric'
    return 'string'

class Field:

    _name:str 
    _type:str 
    _null:int 
    _key:str 
    _default:any 
    _extra:str

    def __init__(self, *args):
        vals = args[0]
        self._name    = vals[0]
        tipo = vals[1].decode('utf-8') if isinstance(vals[1], bytes) else vals[1]
        self._type    = _typed(tipo)
        self._null    = vals[2]
        self._key     = vals[3]
        self._default = vals[4]
        self._extra   = vals[5]

    def getType(self):
        return self._type

    def isNullable(self):
        return self._null == 'YES'

    def isPrimaryKey(self):
        return self._key == 'PRI'

    def getName(self):
        return self._name


class Table:

    _name:str
    _fields:[Field]
    _join:str
    _whereJoin:str
    _primary:Field
    _not_change_fields:[Field]

    def __init__(self, name:str, fields:[], join:str, whereJoin:str):
        
        self._join = join
        self._name = name
        self._whereJoin = whereJoin
        self._primary = None
        self._not_change_fields = []
        self._fields = []

        for field in fields:
            field_obj = Field(field)
            if field_obj.isPrimaryKey():
                self._primary = field_obj
            self._fields.append(field_obj)

    def setJoin(self, join:str):
        self._join = join

    def getWhereJoin(self):
        return self._whereJoin

    def setNotChangeFieldNames(self, fields:[str]):
        
        self._not_change_fields = []

        for fieldstr in fields:

            status = False
            for field in self._fields:
                if field.getName() == fieldstr:
                    status = True
                    self._not_change_fields.append(field)

            if not status:
                self._not_change_fields.append(Field([
                        fieldstr,
                        b'bigint',
                        'NO',
                        'MUL',
                        '',
                        ''
                    ]))

    def getNotChangeFields(self):
        return self._not_change_fields

    def getPrimaryKey(self):
        return self._primary

    def getJoin(self):
        return self._join

    def getName(self):
        return self._name

    def getFields(self, primary:bool = True):
        if primary: return self._fields
        fields = []
        for field in self._fields:
            if field.isPrimaryKey():
                continue
            fields.append(field)

        return fields
        

    def getUpdatableFields(self):
        
        fields = []
        
        for field in self._fields:
            if field.isPrimaryKey() or field.getName() in self._not_change_fields:
                continue
            fields.append(field)

        return fields

    def getFieldByName(self, name:str):
        for field in self._not_change_fields:
            if field.getName() == name:
                return field
        for field in self._fields:
            if field.getName() == name:
                return field
        return False

    def getFieldsName(self, table=True, notPrimary=False):
        
        fieldsNames = ''
       
        for field in self._fields:
            if notPrimary and field.isPrimaryKey():
                continue
            fieldsNames += f" {self._name}."+field.getName()+", " if table else field.getName()+", "
       
        return fieldsNames[:-2]


    def countFields(self, notPrimary=False):
        
        total = 0
        
        for field in self._fields:
            if notPrimary and field.isPrimaryKey():
                continue
            total += 1

        return total
