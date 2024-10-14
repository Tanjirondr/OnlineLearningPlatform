package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
    "sync"
    "time"

    "github.com/joho/godotenv"
)

type Notifier struct {
    apiKey       string
    cache        map[string]string // Adding a simple cache
    cacheMutex   *sync.RWMutex     // Protects cache
    notifyChan   chan string       // Channel for notifications
    shutdownChan chan struct{}     // Channel for graceful shutdown
}

func NewNotifier(apiKey string) *Notifier {
    return &Notifier{
        apiKey:       apiKey,
        cache:        make(map[string]string),
        cacheMutex:   new(sync.RWMutex),
        notifyChan:   make(chan string, 100), // Buffered channel for notifications
        shutdownChan: make(chan struct{}),
    }
}

type Logger struct{}

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
    http.HandleFunc("/health", n.handleHealthCheck) // Health check endpoint
    go n.processNotifications(logger)                // Start processing notifications asynchronously
    logger.Info("Notifier service started on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        logger.Error(fmt.Sprintf("Failed to start server: %s", err.Error()))
    }
}

// Process notifications asynchronously
func (n *Notifier) processNotifications(logger *Logger) {
    for {
        select {
        case notification := <-n.notifyChan:
            // Here we can aggregate and process the notification
            logger.Info(fmt.Sprintf("Processing notification: %s", notification))
            // Simulate notification processing delay
            time.Sleep(2 * time.Second)
        case <-n.shutdownChan:
            return
        }
    }
}

func (n *Notifier) handleNotification(w http.ResponseWriter, r *http.Request) {
    log.Println("Received a notification")

    // Directly send notification to processing channel
    n.notifyChan <- "Notification received" // Placeholder for actual notification data

    fmt.Fprintf(w, "Notification received and will be processed")
}

func (n *Notifier) handleHealthCheck(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Service is up and running")
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