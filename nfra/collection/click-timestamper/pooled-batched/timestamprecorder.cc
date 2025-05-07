#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>

#include <mutex>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include "threadpool.hh"
#include "timestamprecorder.hh"

CLICK_DECLS

int
DataRecorder::configure(Vector<String> &conf, ErrorHandler* errh) {
    String name = "data.csv"; 
    int num_threads = 64;
    int buffer_size = 64;    
    if (Args(conf, this, errh).read_p("NAME", name).
                read_p("THREADS", num_threads).
                read_p("BUFFER_SIZE", buffer_size).
		complete() < 0) {
        return -1;
    }
    _name = name.c_str();
    _pool = new ThreadPool(num_threads, _name, buffer_size);

    return 0;
}


Packet *
DataRecorder::simple_action(Packet *p) {
    // Save the timestamp immediately. We lose cycles on non-IP packets but worth for accurate data
    // std::chrono::high_resolution_clock::time_point stmp = std::chrono::high_resolution_clock::now();
    double timeInSeconds = std::chrono::duration<double>(std::chrono::high_resolution_clock::now().time_since_epoch()).count();

    // Save the packet length
    // uint16_t higher_order_length = p->data()[16];
    // uint16_t lower_order_length = p->data()[17]; 
    // int packet_size = (higher_order_length*16*16) + lower_order_length ;
    int packet_size = (p->data()[16]*16*16) + p->data()[17] ; 
    //  prove before its worth it though
    _pool->enqueue(packet_size, timeInSeconds);

    return p;
}

CLICK_ENDDECLS
EXPORT_ELEMENT(DataRecorder)
