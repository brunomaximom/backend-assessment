package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"

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
	/*
	Atualiza opcode da ativação dependendo do status
	0: cancelada
	1: recusada
	2: aprovada
	*/
	db.Exec("UPDATE t10.ativacao SET opcode="+os.Args[1]+" WHERE id="+os.Args[2]+";")
	if os.Args[1] == "0"{
		fmt.Printf("Ativação %s cancelada.", os.Args[2])
	}
	if os.Args[1] == "1"{
		out, _ := exec.Command("go", "run", "mailServer.go", "denied").Output()
		fmt.Printf("%s", out)
	}
	if os.Args[1] == "2"{
		out, _ := exec.Command("go", "run", "mailServer.go", "approved").Output()
		fmt.Printf("%s", out)
	}
}