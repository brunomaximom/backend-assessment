#!/bin/sh

for i in $(seq 1 30); do
    psql -U postgres -h localhost -p 5432 -d postgres -c "INSERT INTO t10.empresa (cnpj, nome, cc) VALUES ("$i",'empresa"$i"',"$i");"
done

for i in $(seq 1 30); do
    for j in $(seq 1 200); do
        psql -U postgres -h localhost -p 5432 -d postgres -c "INSERT INTO t10.usuario (cpf, nome, empresa, senha) VALUES ("$(((i*200 + j)-200))",'usuario"$(((i*200 + j)-200))"',"$i","$(((i*200 + j)-200))");"
    done
done