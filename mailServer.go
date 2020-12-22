package main

import (
	"fmt"
	"os"
)

func main() {
	if os.Args[1] == "approved" {
		fmt.Println("E-mail enviado para transação aprovada")
	} else if os.Args[1] == "denied" {
		fmt.Println("E-mail enviado para transação recusada")
	}
}