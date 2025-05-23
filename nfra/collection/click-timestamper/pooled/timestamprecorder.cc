#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>
#include "timestamprecorder.hh"
#include <mutex>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include "threadpool.cc"
CLICK_DECLS

std::mutex time_recorder_mtx;


void write_data(int size, double stmp, String filename) {
    
    try{ 
    char colon = ':';
    char comma = ',';
    std::ofstream outputFile;
    
    // Get full range of float
    outputFile << std::fixed << std::setprecision(15);


    time_recorder_mtx.lock();

    // Open the file as append (this is why we delete data in setup)
    //   We could make an init object I guess. But this is 
    //   solution for now
    outputFile.open(filename.c_str(), std::ios::app | std::ios::binary);
    if (!outputFile) { click_chatter("Failed to open file"); }

       
    // Write the length as a dec number for ease of reading
    outputFile << std::to_string(size);
    outputFile.write(&colon, sizeof(char));
    outputFile << stmp;
    outputFile.write(&comma, sizeof(char));
    outputFile.close();

    time_recorder_mtx.unlock();
    }
    catch(const std::exception& e) {
         std::cout << "Caught exception \"" << e.what() << "\"\n";
    }
       
}


int
DataRecorder::configure(Vector<String> &conf, ErrorHandler* errh) {
    String name = "data.csv"; 
    int num_threads = 64;
        if (Args(conf, this, errh).read_p("NAME", name).
                read_p("THREADS", num_threads).complete() < 0) {
        return -1;
    }
    _name = name;
    _pool = new ThreadPool(num_threads);
    return 0;
}


Packet *
DataRecorder::simple_action(Packet *p) {
    // Save the timestamp immediately. We lose cycles on non-IP packets but worth for accurate data
    std::chrono::high_resolution_clock::time_point stmp = std::chrono::high_resolution_clock::now();
    double timeInSeconds = std::chrono::duration<double>(stmp.time_since_epoch()).count();

    // Verify the packet is of type IPv4
    // Yes, I can reduce but easier to understand 4 normies
    // if (!(p->data()[12] == 0x08 && p->data()[13] == 0x00)) { return p; }

    // Save the packet length
    uint16_t higher_order_length = p->data()[16];
    uint16_t lower_order_length = p->data()[17]; 
    int packet_size = (higher_order_length*16*16) + lower_order_length ;
    
    // Now lets save the data
    // std::thread tmpThread(write_data, packet_size, timeInSeconds, _name);
    // tmpThread.detach();
    
    // We could get res from this but we won't
    _pool->enqueue(write_data, packet_size, timeInSeconds, _name);

    return p;
}

CLICK_ENDDECLS
EXPORT_ELEMENT(DataRecorder)
