#ifndef CLICK_TIMESTAMPRECORDER_HH
#define CLICK_TIMESTAMPRECORDER_HH

#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>
#include <click/batchelement.hh>
#include <click/string.hh>

#include <string>

CLICK_DECLS

class DataRecorder: public SimpleElement<DataRecorder> { public:

    DataRecorder() CLICK_COLD {};

    const char *class_name() const              { return "DataRecorder"; }
    const char *port_count() const              { return PORTS_1_1; }

    int configure(Vector<String> &, ErrorHandler *) CLICK_COLD;

    Packet *simple_action(Packet *);

    std::string _name;
    char* _buffer;
    unsigned int _buffer_index;
    unsigned int _buffer_size;

    int _outputFile;

};

CLICK_ENDDECLS
#endif
