#ifndef CLICK_TIMESTAMPRECORDER_HH
#define CLICK_TIMESTAMPRECORDER_HH
#include <click/batchelement.hh>
#include <click/string.hh>
CLICK_DECLS

class DataRecorder: public SimpleElement<DataRecorder> { public:

    DataRecorder() CLICK_COLD {};

    const char *class_name() const              { return "DataRecorder"; }
    const char *port_count() const              { return PORTS_1_1; }

    int configure(Vector<String> &, ErrorHandler *) CLICK_COLD;

    Packet *simple_action(Packet *);

    String _name;
};

CLICK_ENDDECLS
#endif
