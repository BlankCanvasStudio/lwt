
#ifndef CLICK_MEMORYDETECTOR_HH
#define CLICK_MEMORYDETECTOR_HH

#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>
#include <click/batchelement.hh>
#include <click/string.hh>

#include <chrono>


CLICK_DECLS

class MemoryDetector: public SimpleElement<MemoryDetector> { public:

    DataRecorder() CLICK_COLD {};

    const char *class_name() const              { return "DataRecorder"; }
    const char *port_count() const              { return PORTS_1_1; }

    int configure(Vector<String> &, ErrorHandler *) CLICK_COLD;

    std::chrono::high_resolution_clock::time_point _stmp;
    double* _gap_buffer;
    double _last_arrival;
    double _current_arrival;
    int _packet_size;
    int _gap_index;
    int _buffer_size;
    int _packet_delay;
    double _unnecessary_delay;
    double _unnecessary_sum;
    int _total_packets;
};

CLICK_ENDDECLS
#endif
