FROM golang:1.16-buster as builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY ./api ./api
COPY server.go ./

RUN go build -mod=readonly -v -o /bin/server ./

FROM debian:buster-slim
RUN set -x && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy the binary to the production image from the builder stage.
COPY --from=builder /bin/server /server

# Run the web service on container startup.
CMD ["/server"]