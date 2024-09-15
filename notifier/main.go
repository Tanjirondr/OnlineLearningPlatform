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

type Logger struct {
}

func NewLogger() *Logger {
	return &Logger{}
}

func (l *Logger) Info(msg string) {
	log.Printf("INFO: %s", msg)
}

func (l *Logger) Error(msg string) {
	log.Printf("ERROR: %s", msg)
}

func (n *Notifier) Start(logger *Logger) {
	http.HandleFunc("/notify", n.handleNotification)
	logger.Info("Notifier service started on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		logger.Error(fmt.Sprintf("Failed to start server: %s", err.Error()))
	}
}

func (n *Notifier) handleNotification(w http.ResponseWriter, r *http.Request) {
	log.Println("Processing notification")
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
	logger := NewLogger()
	notifier.Start(logger)
}