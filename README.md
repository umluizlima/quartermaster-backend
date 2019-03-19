# Quartermaster (backend)
> Uma aplicação administrativa para o laboratório CDG Hub do Inatel.

Este repositório contém a aplicação web de backend para a solução Quartermaster,
desenvolvida durante uma Iniciação Científica.

## Desenvolvimento local

Os seguintes comandos preparam o ambiente para desenvolvimento local (necessário Python 3.7):
```sh
> git clone https://github.com/umluizlima/quartermaster-backend.git
> cd quartermaster-backend
> pipenv install
```

Para rodar a aplicação de forma local é útil ativar o modo de desenvolvimento, que habilita informações mais detalhadas de debug e hot reload:
```sh
> export FLASK_ENV=development
> pipenv run flask run
```

## Publicação

O arquivo `Procfile` contido na raiz deste projeto serve para publicar a aplicação de maneira fácil na plataforma [Heroku](https://heroku.com) (será preciso que você
crie uma conta gratuita, caso não possua). Siga as seguintes instruções para publicar sua própria instância:

1. Acesse sua conta no Heroku;
2. No dashboard, clique em `Create new app` (no dropdown `New`);
3. Você pode definir um nome para a aplicação (o link de acesso da aplicação será `https://<nome-da-aplicação>.herokuapp.com/`) ou deixar o campo em branco para que seja usado um valor aleatório. Ignore outros campos e clique em `Create App`;
4. Na tela da aplicação (que agora estará listada em seu dashboard), vá na aba `Resources` e digite `Postgres` em sua barra de pesquisa. Isto fará com que a opção `Heroku Postgres` seja listada. Clique nela e então no botão `Provision` dentro da dialog que aparece (confira que o plano selecionado é o grátis `Hobby Dev - Free`);
5.

## Utilização

Em sua primeira publicação a aplicação não contém nenhum usuário cadastrado. É preciso criar um com privilégios administrativos para que as próximas interações possam ser feitas exclusivamente pela interface de [frontend](https://github.com/umluizlima/quartermaster-frontend). As instruções a seguir mostram como fazê-lo:

1.
