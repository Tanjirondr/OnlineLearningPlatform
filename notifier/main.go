package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
)

type Notifier struct {
	apiKey string
}

func NewNotifier(apiKey string) *Notifier {
	return &Notifier{
		apiKey: apiKey,
	}
}

func (n *Notifier) Start() {
	http.HandleFunc("/notify", n.handleNotification)
	log.Println("Notifier service started on :8080")
	http.ListenAndServe(":8080", nil)
}

func (n *Notifier) handleNotification(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Notification processed")
}

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	apiKey := os.Getenv("API_KEY")
	if apiKey == "" {
		log.Fatal("API_KEY must be set in environment")
	}

	notifier := NewNotifier(apiKey)
	notifier.Start()
}