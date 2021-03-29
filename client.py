from __future__ import print_function
import logging

import grpc
from beautifultable import BeautifulTable
import argparse

from api import tictactoe_pb2
from api import tictactoe_pb2_grpc
import threading

class Client:
    def __init__(self, name, room, addr, insecure=False) -> None:
        if insecure: channel = grpc.insecure_channel(addr)
        else: 
            print(addr)
            credentials = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(addr, credentials)

        self.stub = tictactoe_pb2_grpc.TictactoeStub(channel)
        self.responses = self.stub.PlayStream(generate_messages(name, room))
        self.isX = next(self.responses).isX
        if self.isX: print("ban la x")
        else: print("ban la o")
        self.matrix = init_matrix()
        threading.Thread(target=self.start, daemon=True).start()

    def start(self):
        build_table(self.matrix)
        try:
            for res in self.responses:
                if res.state == 5:
                    print("Vui long cho toi luot ban")
                elif res.state == 6:
                    print("Nuoc di khong hop le")
                elif res.state == 0:
                    print("hoa nhau")
                    self.matrix = init_matrix()
                elif res.state == 1:
                    if self.isX: print("ban da chien thang")
                    else: print("ban da thua")
                elif res.state == 2:
                    if self.isX: print("ban da thua")
                    else: print("ban da chien thang")
                elif res.state == 4:
                    print("vui long cho doi thu")
                elif res.state == 3:
                    if res.isCompetitorSend:
                        if self.isX: self.matrix[res.req.x][res.req.y] = 0
                        else: self.matrix[res.req.x][res.req.y] = 1
                    else:
                        if self.isX: self.matrix[res.req.x][res.req.y] = 1
                        else: self.matrix[res.req.x][res.req.y] = 0
                    build_table(self.matrix)
                print()
        except grpc._channel._Rendezvous as err:
            print(err)

def init_matrix():
    return [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

def build_table(matrix):
    table = BeautifulTable()
    for i in range(3):
        tmp = []
        for j in range(3):
            if matrix[i][j] == -1:
                tmp.append("   ")
            elif matrix[i][j] == 1:
                tmp.append(" x ")
            elif matrix[i][j] == 0:
                tmp.append(" o ")
        table.rows.append(tmp)
    print(table)

def convert_move(move):
    if move == 1:
        return [0, 0]
    elif move == 2:
        return [0, 1]
    elif move == 3:
        return [0, 2]
    elif move == 4:
        return [1, 0]
    elif move == 5:
        return [1, 1]
    elif move == 6:
        return [1, 2]
    elif move == 7:
        return [2, 0]
    elif move == 8:
        return [2, 1]
    elif move == 9:
        return [2, 2]

def generate_messages(name, room):
    yield tictactoe_pb2.MessageRequest(
        id = name,
        init = True,
        room = room
    )
    print("\nEnter your move from 1 to 9 or 'q' to quit: \n")
    while True:
        inp = input()
        if inp == "q":
            break
        try:
            num = int(inp)
        except ValueError:
            continue
        move = convert_move(num)
        yield tictactoe_pb2.MessageRequest(
            id = name,
            init = False,
            room = room,
            x = move[0],
            y = move[1]
        )

if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--room', type=str, help='Enter your room', required=True)
    parser.add_argument('--name', type=str, help='Enter your name', required=True)
    parser.add_argument('--addr', type=str, help='Address server ip:port', required=False, default="localhost:1699")
    parser.add_argument('--insecure', dest='insecure', action='store_true')
    parser.set_defaults(insecure=True)
    args = parser.parse_args()
    client = Client(args.name, args.room, args.addr, args.insecure)
    from time import sleep
    while True:
        sleep(10)