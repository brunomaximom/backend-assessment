# Como o problema foi entendido
Haveria 30 empresas parceiras com um número próprio de usuários cada uma - coloquei 200 para cada uma totalizando 6000 usuários no banco. A origem e o destino do evento da ativação seria respectivamente o usuário logado que está solicitando a ativação e o destino que seria uma das 30 empresas.

# Como a solução foi implementada
Abstraí informações como valor da compra ou produto para simplificar a solução e numerei ambos os cpfs (chave primaria da tabela usuario) e senhas dos usuários de 1 a 6000 para facilitar o teste da solução, bem como numerei os cnpjs (chave primaria da tabela empresa) de 1 a 30. A data do evento foi obtida por time.Now() no producer.go. Também para facilitar os testes manuais, todas as requisições são usando método GET.

## Motivações
Quis criar parte da solução em Go e parte em Python (utilizando o Flask) pelos seguintes motivos:
1. treinar a sintaxe de Go;
2. reduzir o código Python para apenas receber as requisições e realizar a autenticação, eventos como recusar/aprovar, criar e cancelar a solicitação seriam realizados fora da API propositalmente;
3. conhecer um ORM para Go;
4. facilitar a execução em paralelo através da API de várias programas em Go dependendo da quantidade de solicitações;

## O processo de implementação
A implementação foi realizada de baixo pra cima, começando do mailServer.go que apenas printa uma mensagem dizendo que um e-mail foi enviado, posteriormente escrevi o produtor e consumidor sucedido pela API e, por fim, implementando a autenticação na API. Não consegui fazer funcionar o pacote flask-jwt instalado com o pip (e acabei perdendo muito tempo tentando), mas consegui utilizar o flask-jwt-extended com sucesso.

## O banco de dados
O banco de dados usado foi só o PostgreSQL, utilizando a role 'postgres' e database 'postgres', mas com um schema de nome 't10'. O acesso ao banco é sem senha e a configuração para acessá-lo sem senha está em pg_hba.conf:
local   all             postgres                                trust
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust

# Como executar
## Dependências


# TODO
Faltou criar os casos de teste
Faltou testar se o requisito não-funcional de 10reqs/s é cumprido
