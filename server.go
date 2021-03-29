package main

import (
	"io"
	"log"
	"net"
	"os"

	"google.golang.org/grpc"

	proto "github.com/anhdhbn/soa/api/tictactoe"
)

var (
	logger = log.New(os.Stdout, "Main server: ", log.Ldate|log.Ltime)
)

type Connection struct {
	stream proto.Tictactoe_PlayStreamServer
	id     string
	active bool
	error  chan error
}

type GameServer struct {
	Connection []*Connection
	Rooms      map[string][]string
	States     map[string][][]string
	Turns      map[string]string
}

func checkWinStep(arr []int) bool {
	sums := [8]int{0, 0, 0, 0, 0, 0, 0, 0}

	sums[0] = arr[2] + arr[4] + arr[6]
	sums[1] = arr[0] + arr[3] + arr[6]
	sums[2] = arr[1] + arr[4] + arr[7]
	sums[3] = arr[2] + arr[5] + arr[8]
	sums[4] = arr[0] + arr[4] + arr[8]
	sums[5] = arr[6] + arr[7] + arr[8]
	sums[6] = arr[3] + arr[4] + arr[5]
	sums[7] = arr[0] + arr[1] + arr[2]
	for _, v := range sums {
		if v == 3 {
			return true
		}
	}
	return false
}

func checkDrawn(states [][]string) bool {
	for _, row := range states {
		for _, idState := range row {
			if idState == "" {
				return false
			}
		}
	}
	return true
}

func checkWin(s *GameServer, room string) string {
	for _, id := range s.Rooms[room] {
		arrCheck := make([]int, 0)
		for _, row := range s.States[room] {
			for _, idState := range row {
				if id == idState {
					arrCheck = append(arrCheck, 1)
				} else {
					arrCheck = append(arrCheck, 0)
				}
			}
		}

		if tmp := checkWinStep(arrCheck); tmp {
			return id
		}
	}

	if tmp := checkDrawn(s.States[room]); tmp {
		return "-"
	}
	return "@"
}

func broadcastState(req *proto.MessageRequest, conn *Connection, s *GameServer) {
	if conn.active {
		mess := proto.MessageResponse{
			Req:              req,
			State:            proto.MessageResponse_NOT_FINISHED,
			IsCompetitorSend: (conn.id != req.Id),
		}

		err := conn.stream.Send(&mess)

		// check move
		if winner := checkWin(s, req.Room); winner != "@" {
			mess2 := proto.MessageResponse{}
			if s.Rooms[req.Room][0] == winner {
				mess2.State = proto.MessageResponse_X_WINS
			} else if s.Rooms[req.Room][1] == winner {
				mess2.State = proto.MessageResponse_O_WINS
			} else {
				mess2.State = proto.MessageResponse_DRAWN
			}
			err = conn.stream.Send(&mess2)
		}
		logger.Printf("Room: %s => Sending message to: %v", req.Room, conn.id)

		if err != nil {
			logger.Printf("Error with Stream: %v - Error: %v", conn.stream, err)
			conn.active = false
			conn.error <- err
		}
	}
}
func checkMove(x int32, y int32) bool {
	if x > 2 || x < 0 {
		return false
	}
	if x > 2 || y < 0 {
		return false
	}
	return true
}

func (s *GameServer) PlayStream(stream proto.Tictactoe_PlayStreamServer) error {
	for {
		req, err := stream.Recv()
		if err == io.EOF {
			break
		} else if err != nil {
			return err
		}
		logger.Printf("Recv message from %s", req.Id)
		if req.Init {
			if room, ok := s.Rooms[req.Room]; ok {
				// neu co phong roi thi them vao
				if _, found := Find(room, req.Id); !found {
					// neu chua ton tai id trong list thi them vao
					s.Rooms[req.Room] = append(room, req.Id)
					res := proto.MessageResponse{
						IsX: false,
					}
					stream.Send(&res)
				}

			} else {
				// neu chua co phong thi tao roi them vao
				s.Rooms[req.Room] = []string{req.Id}
				s.Turns[req.Room] = req.Id
				res := proto.MessageResponse{
					IsX: true,
				}
				stream.Send(&res)
			}

			conn := &Connection{
				stream: stream,
				id:     req.Id,
				active: true,
				error:  make(chan error),
			}
			s.Connection = append(s.Connection, conn)
			logger.Printf("Room: %s adding id: %s", req.Room, req.Id)

			// init room if not exist
			if _, ok := s.States[req.Room]; !ok {
				roomState := make([][]string, 3)
				for i := range roomState {
					roomState[i] = make([]string, 3)
				}
				s.States[req.Room] = roomState
			}
		} else {
			// update state
			if len(s.Rooms[req.Room]) == 2 {
				if s.Turns[req.Room] == req.Id {
					if checkMove(req.X, req.Y) {
						s.States[req.Room][req.X][req.Y] = req.Id

						if req.Id == s.Rooms[req.Room][0] {
							s.Turns[req.Room] = s.Rooms[req.Room][1]
						} else {
							s.Turns[req.Room] = s.Rooms[req.Room][0]
						}

						for _, conn := range s.Connection {
							// if req.Id != conn.id {
							// 	go broadcastState(req, conn, s)
							// }
							go broadcastState(req, conn, s)
						}
					} else {
						res := proto.MessageResponse{
							State: proto.MessageResponse_INVALID,
						}
						stream.Send(&res)
					}
				} else {
					res := proto.MessageResponse{
						State: proto.MessageResponse_WAIT_TURN,
					}
					stream.Send(&res)
				}
			} else {
				res := proto.MessageResponse{
					State: proto.MessageResponse_WAITING,
				}
				stream.Send(&res)
			}
		}
	}
	return nil
}

func Find(slice []string, val string) (int, bool) {
	for i, item := range slice {
		if item == val {
			return i, true
		}
	}
	return -1, false
}

func main() {
	connections := make([]*Connection, 0)
	rooms := make(map[string][]string)
	states := make(map[string][][]string)
	turns := make(map[string]string)

	server := &GameServer{connections, rooms, states, turns}
	grpcServer := grpc.NewServer()

	port := os.Getenv("PORT")
	if port == "" {
		port = "1699"
	}

	logger.Printf("Starting on port %s", port)
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		logger.Fatalf("net.Listen: %v", err)
	}

	proto.RegisterTictactoeServer(grpcServer, server)

	if err = grpcServer.Serve(listener); err != nil {
		logger.Fatal(err)
	}
}
