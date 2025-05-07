#include <click/config.h>
#include <click/args.hh>
#include <click/error.hh>
#include <click/timestamp.hh>
#include "myts.hh"
#include <mutex>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
CLICK_DECLS


int
DataRecorder::configure(Vector<String> &conf, ErrorHandler* errh) {
    String name = "data.csv"; 
    if (Args(conf, this, errh).read_p("NAME", name).complete() < 0) {
        return -1;
    }
    _name = name;
    return 0;
}

int
DataRecorder::initialize(ErrorHandler*) {
	_psizes = (uint32_t*) malloc(100000 * sizeof(int));
	_timestamps = (long double*) malloc(100000 *sizeof(long double));
	_counter = 0;
	_initCounter = 0;

	return 0;
}

Packet *
DataRecorder::simple_action(Packet *p) {
	if (_counter >= 100000) {
		dump();
		_counter = 0;
		return p;
	}
	if (_initCounter < 100) {
		_initCounter++;
		return p;
	}

	_psizes[_counter] = p->length();
	_timestamps[_counter] = p->timestamp_anno().doubleval(); 
	_counter++;

	return p;
}

void
DataRecorder::dump() {
    std::ofstream outputFile;
    outputFile.open(_name.c_str(), std::ofstream::app);
    if (!outputFile) { click_chatter("Failed to open file"); }
		
    for (int c = 0; c < _counter; c++) {
	     outputFile << std::setprecision(19) << _timestamps[c] << ',' << _psizes[c] << '\n';
    }
    outputFile.close();
}

int 
DataRecorder::dump_handler(const String& s, Element* e, void *, ErrorHandler* errh)
{
	DataRecorder *dr = (DataRecorder *) e;
	dr->dump();

	return 0;
}

void
DataRecorder::add_handlers()
{
	add_write_handler("dump", dump_handler, 0);
}



CLICK_ENDDECLS
EXPORT_ELEMENT(DataRecorder)
