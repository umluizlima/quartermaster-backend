# Quartermaster (backend)
> Uma aplicação administrativa para o laboratório CDG Hub do Inatel.

Este repositório contém a aplicação web de backend para a solução Quartermaster,
desenvolvida durante uma Iniciação Científica.

## Desenvolvimento local

Os seguintes comandos preparam o ambiente para desenvolvimento local (necessário Python 3.7):
```sh
git clone https://github.com/umluizlima/quartermaster-backend.git
cd quartermaster-backend
pipenv install
```

Para rodar a aplicação de forma local é útil ativar o modo de desenvolvimento, que habilita informações mais detalhadas de debug e hot reload:
```sh
export FLASK_ENV=development
pipenv run flask run
```

## Publicação

Os arquivos `Procfile` e `app.json` contidos na raiz deste projeto servem para publicar a aplicação de maneira fácil na plataforma [Heroku](https://heroku.com) (será preciso que você crie uma conta gratuita, caso não possua). Siga as seguintes instruções para publicar sua própria instância:

1. Clique no botão abaixo para configurar automaticamente a aplicação no Heroku.

  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Você pode escolher um nome específico no campo `App name` ou deixá-lo em branco para gerar um nome aleatório. Clique em `deploy app` para prosseguir com a publicação.

Pronto! Sua instância do quartermaster-backend está criada e rodando no Heroku.
