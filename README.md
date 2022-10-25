# Dados Livres - Plataforma livre de dados abertos

O **Dados Livres** é uma plataforma livre, sem fins lucrativos, para catalogação de fontes de dados abertos e aplicações cívicas por meio de colaboração coletiva. Um dos objetivos do projeto é criar um ambiente que facilite a atuação do público no controle social e na difusão dos dados abertos para os mais diversos fins.

A ideia de desenvolver a plataforma Dados Livres surgiu em 2018, como um projeto de pesquisa no Instituto Federal de Ciência e Tecnologia do Rio Grande do Norte (IFRN). Mantido e fundado pela [Carolina Soares](https://gitlab.com/mariacarolinass) e por [Pedro Baesse](https://gitlab.com/pbaesse). O Dados Livres é disponibilizado como software livre, sob a [licença GNU GPLv3](https://gitlab.com/dados-livres/dados-livres/-/blob/master/LICENSE) e o seu código-fonte disponível aqui no [GitLab](https://gitlab.com/dados-livres/dados-livres/).

Alguns diferenciais do Dados Livres é a praticidade, pois suas fontes de dados abertos e aplicações cívicas são facilmente cadastradas na plataforma sem exigir nenhum conhecimento de código dos seus usuários. Outro diferencial é a ligação de fontes de dados abertos com as aplicações cívicas na sua página de perfil e vice-versa. Entre os planejamentos futuros do projeto é pretenso permitir cadastrar artigos científicos e notícias que utilizam de dados abertos.

A plataforma foi desenvolvida com a linguagem de programação Python juntamente ao Microframework Web Flask. Além disso, o projeto utiliza as tecnologias web HTML, CSS, JavaScript e o framework Bootstrap.

**Visite o nosso site: [dadoslivres.org](https://dadoslivres.org/)**

**[Saiba mais sobre o Dados Livres aqui](https://dadoslivres.org/about)**

## Sumário

* [Como contribuir](#como-contribuir)
* [Como instalar](#como-instalar)
    * [Configurando o projeto](#configurando-o-projeto)
    * [Rodando o projeto](#rodando-o-projeto)
* [Lista de autores](#lista-de-autores)
* [Licença](#licença)
* [Contato](#contato)
* [Redes sociais](#redes-sociais)

## Como contribuir

1. **Cadastro de fontes e aplicações**

    Contribuia com o Dados Livres ajudando no cadastro de fontes de dados abertos ou aplicações cívicas. Primeiro é necessário ter um [cadastro de usuário](https://dadoslivers.org/auth/register_request) na plataforma, ou caso já tenha um cadastro, realizar o [login](https://dadoslivres.org/auth/login). Logo, preencher o forumário de cadastro da [fonte](https://dadoslivres.org/register_source) ou [aplicação](https://dadoslivres.org/register_software) que deseja cadastrar no Dados Livres.
    
2. **Código-fonte**

    Novas funcionalidades, melhorias ou ideias de issues devem ser feitas aqui no [repositório do Dados Livres](https://gitlab.com/dados-livres/dados-livres). Confira o tópico de [como instalar](#como-instalar) o projeto.

    **Utilize o Git para contribuir com o código:**

    Crie uma nova branch para a funcionalidade que irá desenvolver:

    ```sh
    git checkout -b "nome_da_branch"
    ```

    Adicione todos os arquivos criados ou editados:

    ```sh
    git add nome_do_arquivo
    ```

    Salve os arquivos:

    ```sh
    git commit -m "descreva o que editou ou criou"
    ```

    Suba todas as alterações para o GitLab:

    ```sh
    git push --set-upstream origin nome_da_branch
    ```

3. **Saiba mais sobre como contribuir**

    - [Página de como contribuir na plataforma](https://dadoslivres.org/how_to_contribute)
    - [Ideias de contribuição no quadro de tópicos (issues)](https://gitlab.com/dados-livres/dados-livres/-/boards)

## Como instalar

Primeiro faça um fork do projeto! Em seguida clone o repositório que você fez o fork:

```sh
git clone https://gitlab.com/seu-usuario/dados-livres
```

Para entrar no repositório:

```sh
cd dados-livres
```

Instale o ambiente virtual venv:

```sh
sudo apt-get install python3-venv
```

Utilize o comando abaixo para criar o ambiente virtual de nome venv:

```sh
python3 -m venv venv
```

Para entrar no ambiente virtual utilizando Linux:

```sh
source venv/bin/activate
```

Para entrar no ambiente virtual utilizando Windows:

```sh
source venv\Script\activate
```

Agora, instale todas as dependências do projeto salvas no arquivo requirements.txt:

```sh
pip install -r requirements.txt
```

### Configurando o projeto

Crie o banco de dados:

```sh
flask db init
```

Salve a versão criada do banco de dados:

```sh
flask db migrate -m "subindo banco de dados"
```

Atualize o banco de dados:

```sh
flask db upgrade
```

### Rodando o projeto

Para rodar a aplicação utilize o comando:

```sh
flask run
```

Acesse no seu navegador o seguinte endereço abaixo:

```sh
http://localhost:5000/
```

## Lista de autores

- [Carolina Soares](https://mariacarolinass.github.io/carolinasoares/)
- [Pedro Baesse](https://www.pbaesse.net/)

## Licença

O Dados Livres é Licenciado sob Licença GPL-3.0.

## Contato

Dados Livres:

- Comunidade Dados Livres no Telegram: [@dadoslivres](https://t.me/dadoslivres)
- contato@dadoslivres.org

Mantedores do projeto:

- Telegram: [@carols0](https://t.me/carols0) | m.carolina.soares1@gmail.com
- Telegram: [@pbaesse](https://t.me/pbaesse) | pbaesse@gmail.com

## Redes sociais

- [LinkedIn](https://www.linkedin.com/company/dados-livres/)
- [YouTube](https://www.youtube.com/channel/UCo1LRnYUpCXejZAckGvWmGA)
- [Instagram](https://www.instagram.com/dadoslivres/)
- [Twitter](https://twitter.com/dadoslivres)
- [Facebook](https://www.facebook.com/dadoslivres)

![Logo Dados Livres](/dadoslivres-logo.png)
