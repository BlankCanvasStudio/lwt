#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>

#include <vector>
#include <memory>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <functional>
#include <stdexcept>
#include <string>
#include <fstream>
#include <iomanip>
#include <tuple>
#include <unistd.h>
#include <fcntl.h>
#include "timestamprecorder.hh"

CLICK_DECLS

int
DataRecorder::configure(Vector<String> &conf, ErrorHandler* errh) {
    String name = "data.csv"; 
    int buffer_size = 64;    
    if (Args(conf, this, errh).read_p("NAME", name).
                read_p("BUFFER_SIZE", buffer_size).
		complete() < 0) {
        return -1;
    }
    _name = name.c_str();
    _buffer_index = 0;
    _buffer_size = buffer_size;
    _buffer = new char[ _buffer_size * (sizeof(int) + sizeof(double)) ];

    _outputFile = open(_name.c_str(), O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR); 
    if (!_outputFile) { click_chatter("Failed to open file"); }


    return 0;
}

Packet *
DataRecorder::simple_action(Packet *p) {

    int size = p->length();
    double timestamp = p->timestamp_anno().doubleval();

    memcpy(_buffer + _buffer_index, &size, sizeof(int));
    memcpy(_buffer + _buffer_index + sizeof(int), &timestamp, sizeof(double));
    _buffer_index = 
        (_buffer_index + (sizeof(int) + sizeof(double))) 
        % (_buffer_size * (sizeof(int) + sizeof(double)));

    // Might want to improve this to reduce the critical section
    if (_buffer_index == 0) {
        // These arrays should be de-allocated in the workers
        write(_outputFile, _buffer, _buffer_size * (sizeof(int) + sizeof(double)));
    }

    return p;
}

CLICK_ENDDECLS
EXPORT_ELEMENT(DataRecorder)
