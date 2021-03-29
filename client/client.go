package main

import (
	"context"
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"os"

	proto "github.com/anhdhbn/soa/api/tictactoe"
	"github.com/jedib0t/go-pretty/v6/table"

	"log"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

var (
	// client     proto.TictactoeClient
	// wait       *sync.WaitGroup
	logger     = log.New(os.Stdout, "", 0)
	serverAddr = flag.String("server", "", "Server address (host:port)")
	serverHost = flag.String("server-host", "", "Host name to which server IP should resolve")
	insecure   = flag.Bool("insecure", false, "Skip SSL validation? [false]")
	skipVerify = flag.Bool("skip-verify", false, "Skip server hostname verification in SSL validation [false]")
	name       = flag.String("name", "anhdh-go", "Your username")
	room       = flag.String("room", "room1", "Room name")
	matrix     [][]int
	isX        bool
)

func init() {
	flag.Parse()
	log.SetFlags(log.Flags() ^ log.Ltime ^ log.Ldate)
	matrix = initMatrix()
}

func initMatrix() [][]int {
	return [][]int{
		{-1, -1, -1},
		{-1, -1, -1},
		{-1, -1, -1},
	}
}

func printTable(matrix [][]int) {
	t := table.NewWriter()
	t.SetOutputMirror(os.Stdout)
	for _, row := range matrix {
		tmp := make([]string, 0)
		for _, value := range row {
			if value == -1 {
				tmp = append(tmp, "   ")
			} else if value == 1 {
				tmp = append(tmp, " x ")
			} else if value == 0 {
				tmp = append(tmp, " o ")
			}
		}
		t.AppendRow(table.Row{
			tmp[0],
			tmp[1],
			tmp[2],
		})
		t.AppendSeparator()
	}
	t.Render()
}

func handleSend(stream proto.Tictactoe_PlayStreamClient) {
	req2 := proto.MessageRequest{
		Id:   *name,
		Init: true,
		Room: *room,
	}
	stream.Send(&req2)
	logger.Println("\nEnter your move from 1 to 9 or 'q' to quit: ")
	for {
		var move int
		fmt.Scanf("%d", &move)
		req := proto.MessageRequest{
			Id:   *name,
			Init: false,
			Room: *room,
			X:    0,
			Y:    0,
		}
		if move == 1 {
			req.X = 0
			req.Y = 0
		} else if move == 2 {
			req.X = 0
			req.Y = 1
		} else if move == 3 {
			req.X = 0
			req.Y = 2
		} else if move == 4 {
			req.X = 1
			req.Y = 0
		} else if move == 5 {
			req.X = 1
			req.Y = 1
		} else if move == 6 {
			req.X = 1
			req.Y = 2
		} else if move == 7 {
			req.X = 2
			req.Y = 0
		} else if move == 8 {
			req.X = 2
			req.Y = 1
		} else if move == 9 {
			req.X = 2
			req.Y = 2
		}
		stream.Send(&req)
	}
}

func handleRecv(stream proto.Tictactoe_PlayStreamClient, done chan bool) {
	printTable(matrix)
	res, err := stream.Recv()
	if err == io.EOF {
		close(done)
		return
	}
	if err != nil {
		log.Fatalf("can not receive %v", err)
	}
	isX = res.IsX
	if isX {
		logger.Println("Ban la x")
	} else {
		logger.Println("Ban la o")
	}

	for {
		resp, err := stream.Recv()
		if err == io.EOF {
			close(done)
			return
		}
		if err != nil {
			log.Fatalf("can not receive %v", err)
		}
		if resp.State == proto.MessageResponse_WAIT_TURN {
			logger.Println("Vui long cho toi luot ban")
		} else if resp.State == proto.MessageResponse_INVALID {
			logger.Println("Nuoc di khong hop le")
		} else if resp.State == proto.MessageResponse_DRAWN {
			logger.Println("hoa nhau")
			matrix = initMatrix()
		} else if resp.State == proto.MessageResponse_X_WINS {
			if isX {
				logger.Println("Ban da thang")
			} else {
				logger.Println("Ban da thua")
			}
		} else if resp.State == proto.MessageResponse_O_WINS {
			if isX {
				logger.Println("Ban da thua")
			} else {
				logger.Println("Ban da thang")
			}
		} else if resp.State == proto.MessageResponse_WAITING {
			logger.Println("Vui long cho doi doi thu ket noi")
		} else if resp.State == proto.MessageResponse_NOT_FINISHED {
			if resp.IsCompetitorSend {
				if isX {
					matrix[resp.Req.X][resp.Req.Y] = 0
				} else {
					matrix[resp.Req.X][resp.Req.Y] = 1
				}
			} else {
				if isX {
					matrix[resp.Req.X][resp.Req.Y] = 1
				} else {
					matrix[resp.Req.X][resp.Req.Y] = 0
				}
			}
			printTable(matrix)
		}
	}
}

func main() {
	var opts []grpc.DialOption
	if *serverAddr == "" {
		log.Fatal("-server is empty")
	}
	if *serverHost != "" {
		opts = append(opts, grpc.WithAuthority(*serverHost))
	}
	if *insecure {
		opts = append(opts, grpc.WithInsecure())
	} else {
		cred := credentials.NewTLS(&tls.Config{
			InsecureSkipVerify: *skipVerify,
		})
		opts = append(opts, grpc.WithTransportCredentials(cred))
	}

	conn, err := grpc.Dial(*serverAddr, opts...)
	if err != nil {
		logger.Printf("failed to dial server %s: %v", *serverAddr, err)
	}
	defer conn.Close()

	client := proto.NewTictactoeClient(conn)
	stream, err := client.PlayStream(context.Background())
	if err != nil {
		logger.Fatal("error connect: ", err.Error())
	}

	ctx := stream.Context()
	done := make(chan bool)

	go handleSend(stream)
	go handleRecv(stream, done)

	go func() {
		<-ctx.Done()
		if err := ctx.Err(); err != nil {
			log.Println(err)
		}
		close(done)
	}()

	<-done
}

// package main

// import (
// 	"os"

// 	"github.com/jedib0t/go-pretty/v6/table"
// )

// func main() {
// 	t := table.NewWriter()
// 	t.SetOutputMirror(os.Stdout)
// 	t.AppendRow(table.Row{"  ", " x ", " o "})
// 	t.AppendSeparator()
// 	t.AppendRow(table.Row{"  ", " x ", " o "})
// 	t.AppendSeparator()
// 	t.AppendRow(table.Row{"  ", " x ", " o "})
// 	t.AppendSeparator()
// 	t.Render()
// }
