# Como o problema foi entendido
Haveriam 30 empresas parceiras com um número próprio de usuários cada uma - coloquei 200 para cada uma totalizando 6000 usuários no banco. A origem e o destino do evento da ativação seria respectivamente o usuário logado que está solicitando a ativação e o destino que seria uma das 30 empresas.

# Como a solução foi implementada
Abstraí informações como valor da compra ou produto para simplificar a solução e numerei ambos os cpfs (chave primaria da tabela usuario) e senhas dos usuários de 1 a 6000 para facilitar o teste da solução, bem como numerei os cnpjs (chave primaria da tabela empresa) de 1 a 30. A data do evento foi obtida por time.Now() no producer.go. Também para facilitar os testes manuais, todas as requisições são usando método GET.

## Motivações
Quis criar parte da solução em Go e parte em Python (utilizando o Flask) pelos seguintes motivos:
1. treinar a sintaxe de Go;
2. reduzir o código Python para apenas receber as requisições e realizar a autenticação, eventos como recusar/aprovar, criar e cancelar a solicitação seriam realizados fora da API propositalmente;
3. conhecer um ORM para Go;
4. facilitar a execução em paralelo através da API de várias programas em Go dependendo da quantidade de solicitações;

## O processo de implementação
A implementação foi realizada de baixo pra cima, começando do mailServer.go que apenas printa uma mensagem dizendo que um e-mail foi enviado, posteriormente escrevi o produtor e consumidor sucedido pela API e, por fim, implementando a autenticação na API. Não consegui fazer funcionar o pacote flask-jwt instalado com o pip (e acabei perdendo muito tempo tentando), mas consegui utilizar o flask-jwt-extended com sucesso. Para utilizar este pacote, reaproveitei o código de exemplo do próprio site https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/  

## O banco de dados
O banco de dados usado foi só o PostgreSQL, utilizando a role 'postgres' e database 'postgres', mas com um schema de nome 't10'. O acesso ao banco é sem senha e a configuração para acessá-lo sem senha está em pg_hba.conf:
1. local   all             postgres                                trust  
2. local   all             all                                     trust  
3. host    all             all             127.0.0.1/32            trust  
4. host    all             all             ::1/128                 trust  

Para ter uma ideia de como ele é acessado, olhe o script que usei para populá-lo nomeado como populaBanco.sh  
O arquivo de dump do banco também foi adicionado no repositório, nomeado postgres_dump.txt

## Virtualenv
A API roda em uma venv com todas as dependências satisfeitas. Caso tenha problemas com a venv importada no repositório, crie uma do zero com:  
```$ python3 -m venv backend-assessment```  
Todos os códigos estão no diretório raíz da venv, ou seja, em backend-assessment.  

# Como executar
## Dependências
### No sistema operacional (considerando distribuições Linux baseadas em Debian)  
```# apt install golang postgresql python3 python3-dev python3-pip```  
Não esquecer de configurar o /etc/postgresql/11/main/pg_hba.conf de acordo com a configuração citada anteriormente.  

### Na virtualenv  
```$ source bin/activate```  
```$ pip install flask flask-jwt-extended psycopg2 requests```  
Tenha certeza que os arquivos api.py, consumer.go, producer.go e mailServer.go estão no mesmo diretório raíz da venv. Então rode o flask:  
```export FLASK_APP=api.py```  
```flask run```  

### Golang
Seguir as instruções de instalação do ORM go-pg em https://github.com/go-pg/pg  

# TODO
1. Faltou criar os casos de teste;
2. Faltou testar se o requisito não-funcional de 100reqs/s é cumprido;
