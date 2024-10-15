### API para cadastro de tarefas
## [Link para api na aws](https://api.vtrcordeiro.online/)

> Obs.: commits em inglês.

API desenvolvida em python com flask e alguns outros frameworks, página que usufrui da api: [github](https://github.com/VitorCdSouza/web-page) e [deploy aws](https://vtrcordeiro.online/) (restrições para acesso externo).

Funções simples: login, cadastro, crud de tarefas com atualizaçã do status.

## Caminhos (todos necessitam de token junto a requisição):

GET      get all                  https://api.vtrcordeiro.online/todos (parametros: ?per_page= ?page=)

GET      get by id                https://api.vtrcordeiro.online/todos/<id>

POST     new todo                 https://api.vtrcordeiro.online/todos/ (body: title, description, status)

PUT      update todo status       https://api.vtrcordeiro.online/todos/<id> (body: status)

DELETE   delete todo              https://api.vtrcordeiro.online/todos/<id>
