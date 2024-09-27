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
    apiKey     string
    cache      map[string]string // Adding a simple cache
    cacheMutex *sync.RWMutex     // Protects cache
}

func NewNotifier(apiKey string) *Notifier {
    return &Notifier{
        apiKey:     apiKey,
        cache:      make(map[string]string),
        cacheMutex: new(sync.RWMutex),
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
    logger.Info("Notifier service started on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        logger.Error(fmt.Sprintf("Failed to start server: %s", err.Error()))
    }
}

// Demonstrates a simple "batching" strategy - a placeholder for more complex logic
func (n *Notifier) aggregateNotifications(notifications []string) {
    // Imagine this function batches notifications and sends them out every X seconds
    // Placeholder: details on actual batching and sending logic to be implemented
}

// Example caching mechanism in action
func (n *Notifier) getCachedResponse(key string) (string, bool) {
    n.cacheMutex.RLock()
    defer n.cacheMutex.RUnlock()
    value, found := n.cache[key]
    return value, found
}

func (n *Notifier) setCache(key string, value string) {
    n.cacheMutex.Lock()
    defer n.cacheMutex.Unlock()
    n.cache[key] = value
}

func (n *Notifier) handleNotification(w http.ResponseWriter, r *http.Request) {
    log.Println("Processing notification")
    // Example of using cache
    if val, found := n.getCachedResponse("key"); found {
        fmt.Fprintf(w, "Cached: %s", val)
        return
    }

    // Process and respond to notification here
    // *Actual API call or calculation would go here*

    // Cache the response (simplified example)
    n.setCache("key", "Notification processed")

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