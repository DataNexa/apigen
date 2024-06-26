# Config

Configura a forma como banco de dados será lido:

```typescript

{
    output:string,
    database:{
        user:string,
        password:string,
        host:string,
        db:string
    },
    middlewares:{
        slug:{
            import:string,
            value:string
        }
    }
    services:[
        {
            name:string,
            table:string,
            foreign: boolean | string[] | null,
            ignore_functions:string[] | null,
            api_functions:[
                {
                    func:string,
                    middlewares:string[] | null, // contem as slugs do middewar que será usado
                }
            ]
        }
    ]
}

```

Explicando tudo:

- **output**
Local da saida dos codigos gerados

- **database** 
É a configuração do banco de dados. Se não houver uma, gera um erro.


- **services** 
As tabelas que serão lidas e os serviços que serão gerados da seguinte forma:

-- name 
    Não pode ser nulo. É o nome da tabela que será lida.

-- foreign 
- true (default) - Todas as tabela extrangeira serão lidas também. Incluindo tabelas que não estão relacionadas no campo da tabela atual.
- false - Não vai ler nenhuma tabela
- string[] - Vai ler apenas as tabelas configuradas neste array

-- api_functions
    Quando não há uma configuração definida, todas as funções disponíveis serão configuradas com rotas. São elas:
    `{ 'list', 'unique', 'create', 'update', 'delete' }`
    Se forem definidas apenas as definições serão lidas a não ser que tenha sido configurado o ignore functions.

- func - nome da função escolhida
- method - é o tipo de metodo (post, get, put, delete)
- middlewares - serão injetados na rota, é necessário inserir exatamente o nome do middleware completo em string do import
