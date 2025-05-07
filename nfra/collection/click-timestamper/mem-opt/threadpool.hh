
#ifndef CLICK_THREADPOOL_H
#define CLICK_THREADPOOL_H

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

CLICK_DECLS

class ThreadPool {
    public:
        ThreadPool(size_t threads, std::string filename, int buffer_entries);
        void enqueue(int size, double timestamp);
        ~ThreadPool();
    private:
        // need to keep track of threads so we can join them
        std::vector < std::thread > workers;
        // The actual data stores
        std::vector < char* > data;
        // This is the data buffer information
        int _buffer_size;
        char* _large_buffer;
        int _buffer_index;

        // synchronization
        std::mutex queue_mutex;
        std::mutex file_mutex;
        std::condition_variable condition;

        // file writing materials
        void write_datapoint(char* data);
        std::string _filename;
        int outputFile;
        bool stop;
};

CLICK_ENDDECLS

#endif


