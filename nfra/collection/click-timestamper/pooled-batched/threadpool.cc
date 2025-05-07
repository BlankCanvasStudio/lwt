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
#include "threadpool.hh"

CLICK_DECLS

// the constructor just launches some amount of workers
ThreadPool::ThreadPool(size_t threads, std::string filename, int buffer_entries) : stop(false)
{
    _filename = filename;
    _buffer_size = buffer_entries;
    
    _int_buffer = new int[_buffer_size];
    _double_buffer = new double[_buffer_size];
    _buffer_index = 0;

    // outputFile << std::fixed << std::setprecision(15);
    outputFile.open(filename.c_str(), std::ios::binary | std::ios::app);
    // outputFile.rdbuf()->pubsetbuf(nullptr, 0);
    outputFile.rdbuf()->pubsetbuf(nullptr, 8196);
    if (!outputFile) { click_chatter("Failed to open file"); }

    for(size_t i = 0;i < threads; i++) {
        workers.emplace_back([this] {
            for(;;) {
                std::tuple< int*, double* > data_point;
                
                // Critical section for reading from queue
                {
                    std::unique_lock<std::mutex> lock(this->queue_mutex);
                    this->condition.wait(lock,
                        [this] { 
                            return this->stop || !this->data.empty(); 
                        }
                    );
                    if(this->stop && this->data.empty())
                        return;
                    data_point = std::move(this->data.front());
                    this->data.erase(this->data.begin());
                }

                // Split the tuple and write it
                this->write_datapoint(std::get<0>(data_point), 
                        std::get<1>(data_point));
            }
        });
    }
}


void ThreadPool::write_datapoint(int* sizes, double* times) {
    // Critical section to write the data to the file
    // There actually might be a VERY cheeky memcopy that we could do to speed this up quite a bit
    char buffer[sizeof(int) + sizeof(double) + 1];
    {
        file_mutex.lock();
        
        for (int i = 0; i < _buffer_size; i++) {

            // outputFile << std::setw(4) << std::setfill('0') << std::to_string(sizes[i]);
            // outputFile << reinterpret_cast<const char*>(&sizes[i]) << reinterpret_cast<const char*>(&times[i]) << std::endl;
            // outputFile << reinterpret_cast<const char*>(&times[i]);
            // outputFile.write(reinterpret_cast<const char*>(&sizes[i], sizeof(int)));
            // outputFile.write(&colon, sizeof(char));
            // outputFile << colon << reinterpret_cast<const char*>(&times[i]) << comma << std::endl;
            // outputFile.write(reinterpret_cast<const char*>(&times[i], sizeof(double)));
            // outputFile << times[i];
            // outputFile.write(&comma, sizeof(char));
            // outputFile.write(&comma, sizeof(char));
            // outputFile << std::endl;
            // memcpy(buffer, &sizes[i], sizeof(int));
            // memcpy(buffer + sizeof(int), &times[i], sizeof(double));
            // outputFile.write(buffer, sizeof(int) + sizeof(double) + 1);
            outputFile.write(reinterpret_cast<const char*>(&sizes[i]), sizeof(int));
            outputFile.write(reinterpret_cast<const char*>(&times[i]), sizeof(double));

}

        file_mutex.unlock();

        // End of data buffer life cycle. Make sure to deallocate
        delete[] sizes;
        delete[] times;

    }
}

// add new work item to the pool
void ThreadPool::enqueue(int size, double timestamp) {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);

        // don't allow enqueueing after stopping the pool
        if(stop)
            throw std::runtime_error("enqueue on stopped ThreadPool");
        
        _int_buffer[_buffer_index] = size;
        _double_buffer[_buffer_index] = timestamp;
        _buffer_index = (_buffer_index + 1) % _buffer_size;
        // Might want to improve this to reduce the critical section
        if (_buffer_index == 0) {
            // These arrays should be de-allocated in the workers
            data.emplace_back(_int_buffer, _double_buffer);
            _int_buffer = new int[_buffer_size];
            _double_buffer = new double[_buffer_size];
            condition.notify_one();
        }
    }
}

// the destructor joins all threads
ThreadPool::~ThreadPool()
{
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        stop = true;
    }
    condition.notify_all();
    for(std::thread &worker: workers)
        worker.join();
    outputFile.close();
}

CLICK_ENDDECLS
ELEMENT_PROVIDES(ThreadPool)

