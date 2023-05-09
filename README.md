## Documentação da API
Developed Market API é uma API RESTFul desenvolvida em pyhton, com django, cujo principal objetivo é sustentar a plataforma de e-commerce, com mesmo nome. 
Possuindo três níveis de acesso e permissão (Admin, Seller e Client), a aplicação permite criar e atualizar usuários, criar produtos e movimentar seu estoque, 
adicionar produtos a um carrinho de compras e realizar pedidos. Também é possivel listar pedidos realizados ou vendidos e gerar relatórios de vendas em pdf.

Este repositório contém o código-fonte e os Endpoints das rotas.

## Tabela de Conteúdos

- [Visão Geral](#1-visão-geral)
- [Diagrama ER](#2-diagrama-er)
- [Início Rápido](#3-início-rápido)
    - [Criando o ambiente virtual](#31-criando-o-ambiente-virtual)
    - [Ativando o ambiente virtual](#32-ativando-o-ambiente-virtual)
    - [Instalar as dependências](#33-instalar-as-dependências)
    - [Variáveis de Ambiente](#34-variáveis-de-ambiente)
    - [Migrations](#35-migrations)
    - [Rodando a API](#36-rodando-a-api)
- [Estrutura da API](#4-estrutura-da-api)

---

## 1. Visão Geral
Visão geral do projeto, um pouco das tecnologias usadas.

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [drf-spectacular](https://pypi.org/project/drf-spectacular/)
- [Swagger](https://swagger.io/)

URL base da aplicação: http://localhost:8000/api/

---

## 2. Diagrama ER
Diagrama ER da API definindo bem as relações entre as tabelas do banco de dados.

![Diagrama do projeto com suas relações!](https://i.ibb.co/vvTx0hh/Projeto-em-grupo-m5-drawio.png "Developed-Market-API")

---

## 3. Início rápido
[ Voltar para o topo ](#documentação-da-api)

### 3.1. Criando o ambiente virtual

Clone o projeto em sua máquina e crie um ambiente virtual:

```
python -m venv venv
```
### 3.2. Ativando o ambiente virtual:

Linux:
```
source venv/bin/activate
```

Windows (Powershell):

```
.\venv\Scripts\activate
```

Windows (Git Bash):

```
source venv/Scripts/activate
```
### 3.3. Instalar as dependências:

```
pip install -r requirements.txt
```
### 3.4. Variáveis de Ambiente
Crie um arquivo **.env**, copiando o formato do arquivo **.env.example**:

```
cp .env.example .env
```

Configure suas variáveis de ambiente com suas credenciais do Postgres e uma nova database da sua escolha. Configure também as variáveis do servidor para envio de emails.

### 3.5. Migrations

Execute as migrations com o comando:

```
python manage.py migrate
```

### 3.6. Rodando a API

Para rodar a API localmente use o comando:

```
python manage.py runserver
```
## 4. Estrutura da API

[ Voltar para o topo ](#tabela-de-conteúdos)

É possivel acessar a documentação da API criada com Swagger pelo link abaixo:

[Developed-Market-API-Documentação](https://app.swaggerhub.com/apis-docs/NETOIFPE/Developed-Market-API/1.0.0#/)

Outra forma de acessar a documentação da API é através do link local, quando a API está em execução:

[Developed-Market-API-Documentação-local](http://http://localhost:8000/api/docs/swagger-ui/)

Essa documentação descreve os recusos que a API possuí, como Endpoints, exemplos de requisição, exemplos de retorno e metodos de autenticação

## Autor

- [@Antonio](https://github.com/AntonioSantosBJPE)
- [@Paola](https://github.com/paolarosa)
- [@Lucas](https://github.com/LucasRodrigues23)
