package main

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

func init() {
	if err := godotenv.Load(); err != nil {
		fmt.Println("No .env file found")
	}
}

type Notification struct {
	Message string
}

type User struct {
	Email string
}

func sendNotification(user User, notification Notification) {
	fmt.Printf("Sending notification to %s: %s\n", user.Email, notification.Message)
}

func notifyAllUsersAboutNewCourse(users []User, courseName string) {
	notification := Notification{Message: fmt.Sprintf("New course available: %s", courseName)}
	for _, user := range users {
		sendNotification(user, notification)
	}
}

func notifyAllUsersAboutCourseUpdate(users []User, courseName string) {
	notification := Notification{Message: fmt.Sprintf("Course updated: %s", courseName)}
	for _, user := range users {
		sendNotification(user, notification)
	}
}

func main() {
	users := []User{
		{Email: "user1@example.com"},
		{Email: "user2@example.com"},
	}

	notifyAllUsersAboutNewCourse(users, "Go Programming")
	notifyAllUsersAboutCourseUpdate(users, "Advanced Go Programming")
}