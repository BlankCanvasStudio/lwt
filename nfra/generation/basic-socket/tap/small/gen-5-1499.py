#!/bin/python3

import socket
import time
import random
import string
import multiprocessing
import threading


class TrafficGenerator:

    def __init__(self, ip, rcv_port = 5832, rcv_buf_size = 8, 
                    gen_pac_size = 500, mode = "TCP"):
        self.ip = str(ip)
        self.rcv_port = rcv_port
        self.rcv_buf_size = rcv_buf_size
        self.gen_pac_size = gen_pac_size
        self.sock = None
        self.mode = mode

    def __del__(self):
        if self.sock is not None:
            self.sock.close()

    
    def connect(self):
        sock_type = socket.SOCK_STREAM if \
            self.mode == "TCP" else sock.SOCK_DGRAM
        if self.sock is not None:
            self.sock.close()
        self.sock = socket.socket(socket.AF_INET, sock_type)
        self.sock.connect((self.ip, self.rcv_port))



    def rcv_data(self):
        recieved_data = b''
        while True:
            data = self.sock.recv(self.rcv_buf_size)
            if not data:
                break
            recieved_data += data
        return recieved_data


    def gen_data(self, size = None):
        if size is None: size = self.gen_pac_size
        d = ''.join(random.choice(string.printable) for _ in range(size))
        return d.encode()


    def send_packet(self, size = None):
        if size is None: size = self.gen_pac_size
        self.sock.sendall(self.gen_data(size))


    def traffic(self, size = None, packets = 1):
        if size is None: size = self.gen_pac_size
        self.connect()
        for _ in range(packets):
            self.send_packet(size)
            self.rcv_data()


def main():
    ip = '10.0.5.2'
    rcv_port = 5832
    gen_port = 5833

    connections = [ (ip, rcv_port) for _ in range(0, 1) ]
    processes = []
    objects = []

    # loops = input('How many runs would you like? ')
    # for _ in range(int(loops)):

    sent = 1
    print('Absolutely hurling data')

    while True:
        for host, port in connections:
            obj = TrafficGenerator(ip, rcv_port, gen_pac_size=1499)

            objects.append(obj)

            p = multiprocessing.Process(target=obj.traffic)
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()

        del objects
        del processes
        objects = []
        processes = []

        print('packets set: ', sent)
        sent += 1

        time.sleep(5)


if __name__ == "__main__":
    main()

