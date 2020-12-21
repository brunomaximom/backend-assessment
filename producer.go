package main

import (
	"context"
	"os"
	"time"
	"github.com/go-pg/pg/v10"
	//"github.com/go-pg/pg/v10/orm"
)

const (
	host     = "localhost"
	port     = 5432
	user     = "postgres"
	password = "eu"
	dbname   = "postgres"
  )

func main() {
	db := pg.Connect(&pg.Options{
		Addr: ":5432",
		User: "postgres",
		Password: "eu",
		Database: "postgres",
	})
	defer db.Close()
	ctx := context.Background()

	if err := db.Ping(ctx); err != nil {
		panic(err)
	}
	data := time.Now().String()
	
	//Cria ativação no banco
	db.Exec("INSERT INTO t10.ativacao (origem, destino, data) VALUES ("+os.Args[1]+", "+os.Args[2]+", '"+data+"');")
}
