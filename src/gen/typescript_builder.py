from config.Config import Config
from util.writer import *
from config.Service import Service
from gen.typescript.builder.repositorie import *
from gen.typescript.builder.services import *

route_templates = "src/gen/typescript/_template_typescript_code"

def get_repo_service(service_name:str):
    template = "import { [#service]_repo, [#service]_i } from '../repositories/[#service].repo'"
    return template.replace("[#service]", service_name)

# gera o arquivo de rota
def gen_router(config:Config, service:Service):

    middlewares = config.getMiddlewares()
    middlewares_selected = []

    import_service = f"import {service.getName()}_service from '../services/{service.getName()}.service'"
    routes = ""

    for func in service.getApiFunctions():
        method = func.getFuncName()
        middlewares_value = ""
        for mid in func.getMiddlewares():

            slugmid = mid.getSlug()
            middlewares_selected.append(slugmid)

            middInfo = middlewares[slugmid]
            injects  = mid.getInject()
            value    = middInfo.getValue()
            k = 0
        
            for inject in injects:
                val = value.replace("${"+str(k)+"}", inject)
                middlewares_value += val+","
        routes += f"    router.post('/{method}', {middlewares_value} {service.getName()}_service.{method})\n"

    routes += "\n    return router"
    middlewares_unique_slugs = set(middlewares_selected)
    import_middlewares = ""

    for mid_slug in middlewares_unique_slugs:
        import_middlewares += middlewares[mid_slug].getImport()+"\n"

    fileRoute = read(route_templates+"/routes/service.route.txt")
    fileRoute = fileRoute.replace("[#import_middlewares]", import_middlewares)
    fileRoute = fileRoute.replace("[#import_service]", import_service)
    fileRoute = fileRoute.replace("[#routes]", routes)

    write('output/routes', service.getName()+'.route.ts', fileRoute)


def gen_repository(service:Service):
    
    functionsTemplate = generateFunctionsRepository(service, route_templates)
    fileRepo = read(route_templates+"/repositories/service.repo.txt")
    fileRepo = fileRepo.replace("[#methods]", functionsTemplate)
    fileRepo = fileRepo.replace("[#service]", service.getName()) 

    table = service.getTable()
    params = ""

    for field in table.getFields(primary=False):
        param   = "    "+field.getName()+":"
        if(field.getType() == 'numeric'):
            param += "number"
        else:
            param += "string"
        params += param+",\n"
    
    fileRepo = fileRepo.replace("[#fields]", params[:-2]) 

    write('output/repositories', service.getName()+'.repo.ts', fileRepo)
    


def gen_service(service:Service):

    functions  = generateFunctionService(service, route_templates) 
    importRepo = get_repo_service(service.getName())
    fileServce = read(route_templates+"/services/service.service.txt")
    fileServce = fileServce.replace("[#repositorie]", importRepo)
    fileServce = fileServce.replace("[#methods]", functions)

    write('output/services', service.getName()+'.service.ts', fileServce)


def init(config:Config):
    
    services = config.getServices()
    
    delete_dir('output/repositories')
    delete_dir('output/services')
    delete_dir('output/routes')

    for service in services:
        gen_repository(service)
        gen_service(service)
        gen_router(config, service)