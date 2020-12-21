package main

import (
	"context"
	"os"
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
	db.Exec("UPDATE t10.ativacao SET opcode="+os.Args[1]+" WHERE id="+os.Args[2]+";")
}