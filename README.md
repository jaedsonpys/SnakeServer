# SnakeServer - Framework Web 🐍

![BADGE](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![BADGE](https://img.shields.io/badge/versão-1.0.0-red)
![BADGE](https://img.shields.io/badge/tipo-framework-green)

Documentação oficial do framework SnakeServer.

## Conteúdo

* [Sobre](#Sobre)
* [Como contribuir](#Como-contribuir)
    * [*Enviar relatórios de segurança*](#Enviar-relatórios-de-segurança)
    * [Pull requests](#Pull-Requests) 
* [Primeiros passos](#Primeiros-passos)
    * [Instalação](#)
    * [Hello World](#Hello-World)
* [Licença](#Licença)

# Sobre

O SnakeServer é um framework web sendo desenvolvido para Python com o ***foco em segurança***. Nele, será possível receber solicitações **GET** e **POST**,
definir headers de resposta, obter parâmetros de URL, retornar páginas HTML e outros tipos de conteúdo, e muitas outras funções.

# Como contribuir

Veja como você pode ajudar no SnakeServer:

## Enviar relatórios de segurança

Um dos nossos princípios é a **segurança**, para isso, semanalmente, **diversos** testes são feitos na última e penúltima versão
lançada, para corrigir erros que possam comprometer o servidor.

Se você tem interesse em ajudar desta forma, acesse o arquivo [PENTEST.txt](https://github.com/jaedsonpys/snake-server-framework/blob/master/PENTEST.txt) para melhores informações.

## Pull Requests

Revise o código, encontre bugs, erros, melhorias no código e faça seu pull request!

Todas as pull request são analisadas o mais rápido possível, sendo aceita caso o que você fez
seja beneficiante para o código.

# Primeiros passos

Aqui daremos o primeiro passo na criação de um servidor utilizando o SnakeServer!

## Hello World

Veja um simples hello world utilizando nosso framework:

```python
from snake import Snake

# Função que retorna um Hello World
def hello():
    return 'Hello World powered by SnakeServer!'

# Instanciando a classe Snake e definindo Host e Port
server = Snake(host='127.0.0.1', port=5500)

# Registrando rota e iniciando servidor
server.add_new_route(name='/', method='POST', target=hello)
server.start()
```

Para entender e aprender mais sobre o SnakeServer, acesse a **documentação oficial**.

# Licença

MIT © 2021 Jaedson Silva
