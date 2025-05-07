#!/bin/python3

import socket
import random
import time
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
        while True:
            for _ in range(packets):
                self.send_packet(size)
                self.rcv_data()
            time.sleep(0.000004)

def main():
    ip = '10.0.6.2'
    rcv_port = 5832
    gen_port = 5833

    connections = [ (ip, rcv_port) for _ in range(0, 1) ]
    processes = []
    objects = []

    # loops = input('How many runs would you like? ')
    # for _ in range(int(loops)):

    print('Absolutely hurling data')

    
    threads = []
    for _ in range(0, 8):
        # This creates a 1000b packet every 10^-5 sec
        # Should be 100Mbps
        obj = TrafficGenerator(ip, rcv_port, gen_pac_size=1000)
        p = threading.Thread(target=obj.traffic)
        p.daemon = True
        threads += [ p ]

    for i in range(0, 4):
        threads[i].start()
        time.sleep(0.000001)
       
    for i in range(0, 4):
        threads[i].join()

if __name__ == "__main__":
    main()

