#!/bin/python3

import copy
import struct
import os
import binascii
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

def load_erik_data(filename):
    arrivals = np.array([], dtype=float)
    sizes = np.array([], dtype=int)
    with open(filename) as fd:
        for line in fd:
            [ arrival , size ] = line.strip().split(',')
            if float(arrival) < 160000:
                continue
            arrivals = np.append(arrivals, float(arrival))
            sizes = np.append(sizes, int(size))
    return sizes, arrivals



def load_full_data(filename):
    arrivals = np.array([], dtype=float)
    sizes = np.array([], dtype=int)
    with open(filename) as fd:
        for line in fd:
            [ size, arrival ] = line.strip().split(':')
            if arrival[-1] == ',': arrival = arrival[:-1]
            arrivals = np.append(arrivals, float(arrival))
            sizes = np.append(sizes, int(size))
    return sizes, arrivals


def load_data(filename):
    arrivals = np.array([], dtype=float)
    with open(filename) as fd:
        for line in fd:
            np.append(arrivals, float(line.split(':')[1]))
    return arrivals
   

def read_sliced_data(filename, start, stop):
    arrivals = np.array([], dtype=float)
    sizes = np.array([], dtype=int)
    with open(filename) as fd:
        # Count lines & reset head pointer
        # Get the time offset
        offset = float(fd.readline().strip()[:-1].split(':')[1])
        fd.seek(0)
        for _ in range(start):
            next(fd)

        lines_read = 0
        for line in fd:
            [ size, arrival ] = line.strip().split(':')
            if arrival[-1] == ',': arrival = arrival[:-1]
            arrivals = np.append(arrivals, float(arrival) - offset)
            sizes = np.append(sizes, int(size))
            lines_read += 1

            if lines_read >= stop:
                break

    return sizes, arrivals
        


def align_time_data(time_data):
    # shift = float(time_data[0])
    time_data -= time_data[0]
    return time_data
 

# This function orders both the sizes and times by arrival times
# since its multi-threaded, theres no gaurantee of order at all
def order_by_arrival_time(sizes, times):
    sort_ref = np.argsort(times)
    sorted_sizes = sizes[sort_ref]
    sorted_times = np.sort(times)
    return sorted_sizes, sorted_times

def generate_gaps_list(x):
    gaps_list = []
    for i in range(0, len(x) - 1):
        gap = x[i+1] - x[i]
        gaps_list += [ gap ]
    return gaps_list


def generate_gaps_dict(x):
    gaps = {}
    for i in range(0, len(x) - 1):
        gap = x[i+1] - x[i]
        if gap not in gaps:
            gaps[gap] = 1
        else:
            gaps[gap] += 1
    return gaps

# This removes noisy gaps and corresponding occurances
def remove_gap_noise(gaps, occurances, thresh = 0.07):
    gaps_fin = []
    occurances_fin = []
    for i, val in enumerate(gaps):
        if val < thresh:
            gaps_fin += [ val ]
            occurances_fin += [ occurances[i] ]
    return gaps_fin, occurances_fin


# Unit for this is seconds
def chop_on_time(data, time, start, stop = None):
    if start >= stop: raise ValueError("Error! chop_on_time start > stop")
    if len(data) != len(time): 
        raise ValueError("Error! chop_on_time len(data) != len(time)")
    if stop is None: stop = len(time)
    data = align_time_data(copy.copy(data))
    # Find start and stop time
    
    start_mask = time >= start
    end_mask = time <= stop
    total_mask = start_mask * end_mask

    return time[total_mask], data[total_mask]


def read_pcap_header(fd):
    data = 1
    # while data is not None:
    for _ in range(0, 32):
        data = fd.read(8) # 32 bit words
        print(data)
    

def read_pcap(file_name):
    # read_pcap_header(fd)
    hex_lines = read_raw_hex(file_name)
    for line in hex_lines[:40]:
        print(line)


def read_raw_hex(file_name):
    fd = open(file_name, 'rb')
    binary_data = fd.read()
    # Calculate the number of 32-bit words
    num_words = len(binary_data) // 4
    # Unpack the binary data into a list of hex strings
    hex_strings = struct.unpack(f"{num_words}I", binary_data)
    hex_digits = [f"{x:08X}" for x in hex_strings]
    
    split = []
    for el in hex_digits:
        split +=  [ el[:4] ]
        split +=  [ el[4:] ]

    return split

def flip_hex(hex_digits):
    # flip around the digits cause endian is fun
    return [ x[2:] + x[:2] for x in hex_digits ]

class PCAPDataPoint:
    def __init__(self, stmp_sec, stmp_min, cap_len, orig_len, packet = None):
        self.stmp_sec = stmp_sec
        self.stmp_min = stmp_min
        self.cap_len = cap_len
        self.orig_len = orig_len
        self.packet = packet

    def __str__(self):
        out = "PCAP Data Point: " + '\n'
        out += '  sec: ' + str(self.stmp_sec) + '\n'
        out += '  min: ' + str(self.stmp_min) + '\n'
        out += '  cap len: ' + str(self.cap_len) + '\n'
        out += '  orig len: ' + str(self.orig_len) + '\n'
        out += 'Packet: ' + str(self.packet) + '\n'
        return out


class ETHPacket():
    def __init__(self, eth_src, eth_dest, eth_type, data):
        self.eth_src = eth_src
        self.eth_dest = eth_dest
        self.eth_type = eth_type
        self.data = data
    
    def __str__(self):
        out = 'Ethernet Packet Header: ' + '\n'
        out += '  dest: ' +  str(self.eth_dest) + '\n'
        out += '  src: ' +  str(self.eth_src) + '\n'
        out += '  type: ' +  str(self.eth_type) + '\n'
        out += 'Ethernet Packet Data: ' + '\n'
        out += str(self.data) + '\n'
        return out
    def __type__(self):
        if type(self.data) is str:
            return 'Ethernet Packet'
        else:
            return type(self.data)


        

class IPv4Packet():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        out = 'IPv4 Packet: ' + '\n'
        joined = ''.join(self.data) 
        out += '\n'.join(
                [joined[i:i+8] for i in range(0, len(joined), 8)]
                )
        return out
    def __repl__(self):
        return self.__str__()
    def __repr__(self):
        return 'IPv4 Packet'



class ARPPacket():
    def __init__(self, data):
        self.data = data
    def __str__(self):
        out = "ARP Packet: " + '\n'
        joined = ''.join(self.data) 
        out += '\n'.join(
                [joined[i:i+8] for i in range(0, len(joined), 8)]
                )
        return out
    def __repr__(self):
        return 'ARP Packet'

class IPv6Packet():
    def __init__(self, data):
        self.data = data
    def __str__(self):
        out = "IPv6 Packet: " + '\n'
        joined = ''.join(self.data) 
        out += '\n'.join(
                [joined[i:i+8] for i in range(0, len(joined), 8)]
                )
        return out
    def __repr__(self):
        return 'IPv6 Packet'



class PCAPReader:
    def __init__(self, filename):
        self.filename = filename
        self.fd = open(self.filename, 'rb')
        # For consistent reading. Nice to have
        self.read_index = 0
        # For the raw data. Set in load
        self.data = None 
        # Header information. Set in read_header
        self.magic_num = None
        self.version = None
        self.snaplen = None
        self.FCS = None
        self.F = None
        self.linktype = None
        # To hold all the packet objects
        # These need to be read in from the data
        self.pcap_data = []

        # Finding EOF cause python doesn't have EOF function
        self.fd.seek(0, os.SEEK_END)
        self.file_size = self.fd.tell()
        self.fd.seek(0)

        self.load()

    def info(self):
        print('PCAP Reader Info: ')
        print('  filename: ', self.filename)
        print('  magic_num: ', self.magic_num)
        print('  snaplen: ', self.snaplen)
        print('  FCS: ', self.FCS)
        print('  F: ', self.F)
        print('  link type: ', self.linktype)

    def types(self):
        out = []
        for el in self.pcap_data:
            if el.packet.data:
                out += [ type(el.packet.data) ]
            else:
                out += [ type(el.packet) ]
        return out

    def times(self, adjust = False):
        tuples = []
        out = []

        if self.magic_num == 'A1B2C3D4': # MICRO SECONDS
            scalar = 1000000
        elif self.magic_num == 'A1B23C4D': # NANO SECONDS
            scalar = 10**9
        else:
            raise ValueError("Invalid Magic Number")

        for el in self.pcap_data:
            sec = int(el.stmp_sec, 16)
            min = int(el.stmp_min, 16)
            tuples += [[sec, min]]

        if adjust: 
            base_sec = int(self.pcap_data[0].stmp_sec, 16)
            base_mini = int(self.pcap_data[0].stmp_min, 16)
            tuples = [ 
                [ x[0] - base_sec, (x[1] - base_mini) ] 
                for x in tuples ]
        
        # Convert tuples to time stamps
        for el in tuples:
            out += [ el[0] + (el[1] / scalar) ]

        return out

    def sizes(self):
        out = []
        for el in self.pcap_data:
            out += [ int(el.orig_len, 16) ]
        return out

    def load(self):
        self.read_pcap_header()
        self.read_packets()

    # This will pretty print packets or data depending on raw flag
    def print(self, length = 1, start = 0, raw = False):
        out = []
        if raw:
            self.fd.seek(start)
            for _ in range(0, length):
                out += [ self.read_word(length = 4, join = True) ]
        else:
            out += self.pcap_data[start:start + length]
        for el in out:
            print(el)

    def read_pcap_header(self):
        self.magic_num = self.read_word(4, join = True, flip = True)
        self.version = self.read_word(4, join = True, flip = True)
        self.read_word(4) # Skip this section. Reserved
        self.snaplen = self.read_word(4, join = True, flip = True)
        tmp = self.read_word(4, flip = True)
        tmp_data = self.read_word(1, join = True, flip = True)
        self.read_word(1) # Skip this blank section
        self.linktype = self.read_word(2, join = True, flip = True)

    def read_word(self, length = 1, flip = False, join = False):
        data = []
        for _ in range(0, length):
            data += self.raw_read(1)
        
        if flip: data = list(reversed(data))
        if join: data = ''.join(data)
        return data

    # This function is to read raw data from the file. Use read_word
    #   so that the re-arranging of data is done correctly
    def raw_read(self, length = 1):
        out = []
        for _ in range(0, length):
            data = self.fd.read(1)
            hex_digits = ''.join([f'{byte:02x}' for byte in data])
            hex_digits = hex_digits.upper()
            out +=  [hex_digits]
        return out

    # PCAPs store timing data before the actual packet. This processes
    #   that information, stores it in PCAPData point and returns it
    def read_packet_preamble(self):
        sec_stmp = self.read_word(4, join = True, flip = True)
        mini_stmp = self.read_word(4, join = True, flip = True)
        cap_len = self.read_word(4, join = True, flip = True)
        orig_len = self.read_word(4, join = True, flip = True)
        return PCAPDataPoint(sec_stmp, mini_stmp, cap_len, orig_len)

    def read_packets(self):
        self.read_index = 12 # Where packets actually start
        # while self.read_index < len(self.data): 
        while self.fd.tell() < self.file_size:
            # Read the header & create data object we are saving
            pcap_data_point = self.read_packet_preamble()
            # Read the packet info and save it into the data point
            pkt = self.read_ethernet_packet(length = pcap_data_point.cap_len)
            pcap_data_point.packet = pkt
            # Save the data point
            self.pcap_data += [ pcap_data_point ]

    def read_ethernet_packet(self, length):
        length = (int(length, 16) - 14)

        eth_dst = self.read_word(6, flip = False, join = True)
        eth_src = self.read_word(6, flip = False, join = True)
        eth_type = self.read_word(2, flip = False, join = True) # flip_hex(self.data[self.read_index])
        eth_packet = ETHPacket(eth_src, eth_dst, eth_type, None)

        if eth_type == '0800':
            eth_packet.data = self.read_ipv4(length)
        elif eth_type == '86DD':
            eth_packet.data = self.read_ipv6(length = length)
        elif eth_type == '0806':
            eth_packet.data = ARPPacket(self.read_word(length))
        else: 
            self.read_word(length)
            print('packet ID failed')

        return eth_packet
    
    def read_ipv4(self, length):
        return IPv4Packet(data = self.read_word(length))

    def read_ipv6(self, length):
        return IPv6Packet(data = self.read_word(length))


class MinPCAPReader:
    def __init__(self, filename):
        self.filename = filename
        self.fd = open(self.filename, 'rb')
        self.read_index = 0
        # For the raw data. Set in load
        self._times = np.array([])
        self._sizes = np.array([])
        self.data = None 
        self.scalar = None
        # Header information. Set in read_header
        self.magic_num = None
        # These need to be read in from the data

        # Finding EOF cause python doesn't have EOF function
        self.fd.seek(0, os.SEEK_END)
        self.file_size = self.fd.tell()
        self.fd.seek(0)

        self.load()

    def times(self, align = False):
        out = self._times
        if align: out = self._times - self._times[0]
        return out

    def sizes(self):
        return self._sizes
    
    def load(self):
        self.read_pcap_header()
        self.read_packets()

    def forward(self, length):
        self.fd.seek(length, 1)

    def read_pcap_header(self):
        self.magic_num = self.read_word(4, join = True, flip = True)
        self.forward(20)
        
        if self.magic_num == 'A1B2C3D4': # MICRO SECONDS
            self.scalar = 1000000
        elif self.magic_num == 'A1B23C4D': # NANO SECONDS
            self.scalar = 10**9
        else:
            raise ValueError("Invalid Magic Number")


    def read_word(self, length = 1, flip = False, join = False):
        data = []
        for _ in range(0, length):
            data += self.raw_read(1)
        
        if flip: data = list(reversed(data))
        if join: data = ''.join(data)
        return data

    # This function is to read raw data from the file. Use read_word
    #   so that the re-arranging of data is done correctly
    def raw_read(self, length = 1):
        out = []
        for _ in range(0, length):
            data = self.fd.read(1)
            hex_digits = ''.join([f'{byte:02x}' for byte in data])
            hex_digits = hex_digits.upper()
            out +=  [hex_digits]
        return out

    # PCAPs store timing data before the actual packet. This processes
    #   that information, stores it in PCAPData point and returns it
    def read_packet_preamble(self):
        sec_stmp = self.read_word(4, join = True, flip = True)
        mini_stmp = self.read_word(4, join = True, flip = True)
        snap_len = self.read_word(4, join = True, flip = True)
        orig_len = self.read_word(4, join = True, flip = True)
        time = int(sec_stmp, 16) + (int(mini_stmp, 16) / self.scalar)
        return time, int(orig_len, 16), int(snap_len, 16)


    def read_packets(self, num = -1, start = 0):
        while self.fd.tell() < self.file_size:
        # for _ in range(0, 5000000):
            # Read the header & create data object we are saving
            time, length, snap_len = self.read_packet_preamble()
            self.forward(snap_len)
            np.append(self._times, time)
            np.append(self._sizes, length)

        
 
class PcapStreamer:

    def __init__(self, filename, buffer_size = 100000, link_bps = 100 * 1000 * 1000, output = None):
        self.filename = filename

        self.arrivals = np.zeros(buffer_size, dtype=np.double)
        self.sizes = np.zeros(buffer_size, dtype=int)
        self.buffer_size = buffer_size

        self.insert_index = 0

        self.file_size = os.path.getsize(filename)

        self.link_bps = link_bps
        
        self.exit = False

        self.output = output

        self.fd = open(self.filename, 'rb') 
        print("filename:", self.filename, '\n')

        self.read_pcap_header()

        time, size, snap = self.read_packet_preamble()
        self.offset = time
        
        # Work around but whatever
        self.fd.seek(0)
        self.read_pcap_header()

    def read_pcap_header(self):
        self.magic_num = self.read_word(4, join = True, flip = True)
        self.forward(20)
        
        if self.magic_num == 'A1B2C3D4': # MICRO SECONDS
            self.scalar = 1000000
        elif self.magic_num == 'A1B23C4D': # NANO SECONDS
            self.scalar = 10**9
        else:
            raise ValueError("Invalid Magic Number")


    def stream(self, callback, skip = 0, align = True):

        while self.fd.tell() < self.file_size:
            # This reading method is correct
            int_val, float_val = self.read()

            if float_val < 10:
                continue

            # print(int_val, float_val)
            if align:
                self.arrivals[self.insert_index] = float_val - self.offset
            else:
                 self.arrivals[self.insert_index] = float_val   
            self.sizes[self.insert_index] = int_val

            callback(self)           
            if self.exit: return

            self.insert_index = ((self.insert_index + 1) 
                                    % self.buffer_size)


    def read_word(self, length = 1, flip = False, join = False):
        data = []
        for _ in range(0, length):
            data += self.raw_read(1)
        
        if flip: data = list(reversed(data))
        if join: data = ''.join(data)
        return data

    # This function is to read raw data from the file. Use read_word
    #   so that the re-arranging of data is done correctly
    def raw_read(self, length = 1):
        out = []
        for _ in range(0, length):
            data = self.fd.read(1)
            hex_digits = ''.join([f'{byte:02x}' for byte in data])
            hex_digits = hex_digits.upper()
            out +=  [hex_digits]
        return out

    # PCAPs store timing data before the actual packet. This processes
    #   that information, stores it in PCAPData point and returns it
    def read_packet_preamble(self):
        sec_stmp = self.read_word(4, join = True, flip = True)
        mini_stmp = self.read_word(4, join = True, flip = True)
        snap_len = self.read_word(4, join = True, flip = True)
        orig_len = self.read_word(4, join = True, flip = True)
        time = int(sec_stmp, 16) + (int(mini_stmp, 16) / self.scalar)
        return time, int(orig_len, 16), int(snap_len, 16)


    def read_packets(self, num = -1, start = 0):
        while self.fd.tell() < self.file_size:
        # for _ in range(0, 5000000):
            # Read the header & create data object we are saving
            time, length, snap_len = self.read_packet_preamble()
            self.forward(snap_len)
            np.append(self._times, time)
            np.append(self._sizes, length)


    def forward(self, length):
        self.fd.seek(length, 1)


    def read(self):
        time, len, snap_len = self.read_packet_preamble()
        self.forward(snap_len)
        return len, time


    # Used for relative indexing datapoints
    def index(self, index):
        new_index = (self.insert_index + index) % self.buffer_size
        if new_index < 0: new_index = self.buffer_size + new_index
        return self.sizes[new_index], self.arrivals[new_index]
       
 
class Streamer:

    def __init__(self, filename, buffer_size = 100000, link_bps = 100 * 1000 * 1000, output = None):
        self.filename = filename

        self.arrivals = np.zeros(buffer_size, dtype=np.double)
        self.sizes = np.zeros(buffer_size, dtype=int)
        self.buffer_size = buffer_size

        self.insert_index = 0

        self.file_size = os.path.getsize(filename)

        self.link_bps = link_bps
        
        self.exit = False

        self.output = output

        with open(self.filename, 'rb') as fd:
            fd.seek(4)
            self.offset = struct.unpack('d', fd.read(8))[0]
            print('offset:', self.offset)

        self.fd = open(self.filename, 'rb') 
        print("filename:", self.filename, '\n')


    def stream(self, callback, skip = 0, align = True):
        self.fd.seek(0)
        self.fd.seek(skip * 12) # 4 byte int with 8 byte double

        while self.fd.tell() < self.file_size:
            # This reading method is correct
            int_val, float_val = self.read()

            if float_val < 10:
                continue

            # print(int_val, float_val)
            if align:
                self.arrivals[self.insert_index] = float_val - self.offset
            else:
                 self.arrivals[self.insert_index] = float_val   
            self.sizes[self.insert_index] = int_val

            callback(self)           
            if self.exit: return

            self.insert_index = ((self.insert_index + 1) 
                                    % self.buffer_size)


    def read(self):
        int_val = int.from_bytes(self.fd.read(4), sys.byteorder)
        float_val = struct.unpack('d', self.fd.read(8))[0]
        return int_val, float_val


    # Used for relative indexing datapoints
    def index(self, index):
        new_index = (self.insert_index + index) % self.buffer_size
        if new_index < 0: new_index = self.buffer_size + new_index
        return self.sizes[new_index], self.arrivals[new_index]
 


class ErikStreamer:

    def __init__(self, filename, buffer_size = 100000, link_bps = 100 * 1000 * 1000, output = None):
        self.filename = filename

        self.arrivals = np.zeros(buffer_size, dtype=np.double)
        self.sizes = np.zeros(buffer_size, dtype=int)
        self.buffer_size = buffer_size

        self.insert_index = 0

        self.file_size = os.path.getsize(filename)

        self.link_bps = link_bps
        
        self.exit = False

        self.output = output

        with open(self.filename, 'r') as fd:
            [ arrival, size ] = fd.readline().split(',')
            self.offset = float(arrival)
            print('offset:', self.offset)

        self.fd = open(self.filename, 'r') 
        print("filename:", self.filename)


    def stream(self, callback, skip = 0, align = True):
        self.fd.seek(0)

        for _ in range(0, skip):
            self.fd.readline()

        for line in self.fd:
            [ float_val, int_val ] = line.split(',')
            if align:
                self.arrivals[self.insert_index] = float(float_val) - self.offset
            else:
                 self.arrivals[self.insert_index] = float(float_val)
            self.sizes[self.insert_index] = int(int_val)

            callback(self)           
            if self.exit: return

            self.insert_index = ((self.insert_index + 1) 
                                    % self.buffer_size)




    def read(self):
        [ float_val, int_val ] = self.rd.readline().split(',')
        return int(int_val), float(float_val)


    # Used for relative indexing datapoints
    def index(self, index):
        new_index = (self.insert_index + index) % self.buffer_size
        if new_index < 0: new_index = self.buffer_size + new_index
        return self.sizes[new_index], self.arrivals[new_index]

