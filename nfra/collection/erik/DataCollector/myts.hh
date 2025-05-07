#ifndef CLICK_DATARECORDER_HH
#define CLICK_DATARECORDER_HH
#include <click/batchelement.hh>
#include <click/string.hh>
CLICK_DECLS

class DataRecorder: public Element { public:
    DataRecorder() CLICK_COLD {};
    const char *class_name() const              { return "DataRecorder"; }
    const char *port_count() const              { return PORTS_1_1; }

    int configure(Vector<String> &, ErrorHandler *) CLICK_COLD;
    int initialize(ErrorHandler *) CLICK_COLD;

    Packet *simple_action(Packet *);

    String _name;

    uint32_t *_psizes;
    long double *_timestamps;
    int _counter;
    int _initCounter;

    static int dump_handler(const String& s, Element* e, void *, ErrorHandler* errh);
    void dump();

    void add_handlers() CLICK_COLD;

};

CLICK_ENDDECLS
#endif

