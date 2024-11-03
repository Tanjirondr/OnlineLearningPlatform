package main

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

func init() {
	if err := godotenv.Load(); err != nil {
		fmt.Printf("No .env file found")
	}
}

type Notification struct {
	Message string
}

type User struct {
	Email string
}

func SendNotification(user User, notification Notification) {
	fmt.Printf("Sending notification to %s: %s\n", user.Email, notification.Message)
}

func NotifyUsersAboutNewCourse(users []User, courseName string) {
	notification := Notification{Message: fmt.Sprintf("New course available: %s", courseName)}
	for _, user := range users {
		SendNotification(user, notification)
	}
}

func NotifyUsersAboutUpdatedCourse(users []User, courseName string) {
	notification := Notification{Message: fmt.Sprintf("Course updated: %s", courseName)}
	for _, user := range users {
		SendNotification(user, notification)
	}
}

func main() {
	users := []User{
		{Email: "user1@example.com"},
		{Email: "user2@example.com"},
	}

	NotifyUsersAboutNewCourse(users, "Go Programming")
	NotifyUsersAboutUpdatedCourse(users, "Advanced Go Programming")
}