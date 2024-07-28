FROM golang:1.16
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o notifier main.go
EXPOSE 8080
CMD ["./notifier"]
