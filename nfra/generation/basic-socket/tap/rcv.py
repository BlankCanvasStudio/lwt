#!/bin/python3

import socket
import threading
import sys


class TrafficResponder:
    def __init__(self, sock, addr, buf_size = 8):
        self.sock = sock
        self.addr = addr
        self.buf_size = buf_size

    def __del__(self):
        try:
            self.sock.close()
        except:
            pass

    def recieve_all(self):
        # Idk why the socket timeouts make it work but necessary
        old_timeout = self.sock.gettimeout()
        self.sock.settimeout(1)
        recieved_data = b''
        while True:
            try:
                data = self.sock.recv(self.buf_size)
                if not data:
                    break
                recieved_data += data
            except socket.timeout:
                break
        self.sock.settimeout(old_timeout)
        return recieved_data


    def send(self, data):
        self.sock.sendall(data.encode())


    def handle_conn(self, threaded = True, **kwargs):
        data = self.recieve_all()
        self.send("ACK")
        self.sock.close()
        sys.exit()



def main():
    ip = '0.0.0.0'
    rcv_port = 5832
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, rcv_port))
    sock.listen(1)

    print(f'listening on {ip}:{rcv_port}')

    while True:
        client_sock, client_addr = sock.accept()
        resp = TrafficResponder(client_sock, client_addr)
        t = threading.Thread(target=resp.handle_conn)
        t.start()



if __name__ == "__main__":
    main()


