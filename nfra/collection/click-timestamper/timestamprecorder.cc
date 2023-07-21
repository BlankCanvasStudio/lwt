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
CLICK_DECLS

std::mutex time_recorder_mtx;

int
DataRecorder::configure(Vector<String> &conf, ErrorHandler* errh) {
    String name = "data.csv"; 
    if (Args(conf, this, errh).read_p("NAME", name).complete() < 0) {
        return -1;
    }
    _name = name;
    return 0;
}


Packet *
DataRecorder::simple_action(Packet *p) {
    // Save the timestamp immediately. We lose cycles on non-IP packets but worth for accurate data
    std::chrono::high_resolution_clock::time_point stmp = std::chrono::high_resolution_clock::now();
    double timeInSeconds = std::chrono::duration<double>(stmp.time_since_epoch()).count();

    // Verify the packet is of type IPv4
    // Yes, I can reduce but easier to understand 4 normies
    if (!(p->data()[12] == 0x08 && p->data()[13] == 0x00)) { return p; }
    
    // Save the packet length
    uint16_t higher_order_length = p->data()[16];
    uint16_t lower_order_length = p->data()[17]; 
    
    // Now lets save the data
    time_recorder_mtx.lock();

    // Open the file as append (this is why we delete data in setup)
    //   We could make an init object I guess. But this is 
    //   solution for now
    std::ofstream outputFile;
    outputFile.open(_name.c_str(), std::ios::app | std::ios::binary);
    if (!outputFile) { click_chatter("Failed to open file"); return p; }

    // Get full range of float
    outputFile << std::fixed << std::setprecision(15);

    char colon = ':';
    char comma = ',';
    
    // Write the length as a dec number for ease of reading
    outputFile << std::to_string((higher_order_length*16*16) + lower_order_length);
    outputFile.write(&colon, sizeof(char));
    outputFile << timeInSeconds;
    outputFile.write(&comma, sizeof(char));
    outputFile.close();

    time_recorder_mtx.unlock();
    return p;
}

CLICK_ENDDECLS
EXPORT_ELEMENT(DataRecorder)
