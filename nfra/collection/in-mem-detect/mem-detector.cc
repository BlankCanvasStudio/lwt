#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>

#include <mutex>
#include <iostream>
#include <cstdint>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <math.h>
#include "mem-detector.hh"

#include <sstream>
#include <cstring>

CLICK_DECLS

int
MemoryDetector::configure(Vector<String> &conf, ErrorHandler* errh) {
    int size = 1048576; // 1Mb
    if (Args(conf, this, errh).read_p("SIZE", buffer_size).
                complete() < 0) {
        return -1;
    }

    // Build gap buffer
    _gap_buffer = new double[size];
    _buffer_size = size;
    // Load the last arrival time as the start of the router (could be wrong through)
    std::chrono::high_resolution_clock::time_point stmp = std::chrono::high_resolution_clock::now();
    _last_arrival = std::chrono::duration<double>(stmp.time_since_epoch()).count();
    // Set the gap index to the first entry
    _gap_index = 0;

    return 0;
}


Packet *
MemoryDetector::simple_action(Packet *p) {
    // Save the timestamp immediately. We lose cycles on non-IP packets but worth for accurate data
    _stmp = std::chrono::high_resolution_clock::now();
    _current_arrival = std::chrono::duration<double>(stmp.time_since_epoch()).count();
    _gap_buffer[_gap_index] = _current_arrival - _last_arrival;
     
    // Calc the packet length
    _packet_size = (p->data()[16]*16*16) + p->data()[17];

    // Calculate the necessary delay (sec/bit) * (bit):
    _packet_delay = (1 / (10 * pow(2, 30))) * (8 * _packet_size);

    // How much of a gap was recorded
    _unnecessary_delay = _gap_buffer - _packet_delay; 

    _unnecessary_sum += _unnecessary_delay;
    
    if (_unnecessary_delay * 10 > (_unnecessary_sum / _total_packets)) 
        { click_chatter("Large gap detection"); }

    _gap_index = ( (_gap_index + 1) % _buffer_size);
    _last_arrival = _current_arrival;

    return p;
}

CLICK_ENDDECLS
EXPORT_ELEMENT(MemoryDetector)

