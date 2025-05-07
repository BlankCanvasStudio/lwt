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
#include "threadpool.hh"

CLICK_DECLS

// the constructor just launches some amount of workers
ThreadPool::ThreadPool(size_t threads, std::string filename, int buffer_entries) : stop(false)
{
    _filename = filename;
    _buffer_size = buffer_entries;
    
    _large_buffer = new char[ _buffer_size * (sizeof(int) + sizeof(double)) ];
    _buffer_index = 0;

    outputFile = open(filename.c_str(), O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR); 
    if (!outputFile) { click_chatter("Failed to open file"); }

    for(size_t i = 0;i < threads; i++) {
        workers.emplace_back([this] {
            for(;;) {
                char* data_point;
                
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
                this->write_datapoint(data_point);
            }
        });
    }
}


void ThreadPool::write_datapoint(char* data) {
    {
        file_mutex.lock();

        write(outputFile, data, _buffer_size * (sizeof(int) + sizeof(double)));

        file_mutex.unlock();

    }

    // End of data buffer life cycle. Make sure to deallocate
    delete[] data;
}

// add new work item to the pool
void ThreadPool::enqueue(int size, double timestamp) {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);

        // don't allow enqueueing after stopping the pool
        if(stop)
            throw std::runtime_error("enqueue on stopped ThreadPool");
        
        // _large_buffer[_buffer_index] = reinterpret_cast<char*>(size);
        // _large_buffer[_buffer_index] = size;
        // _large_buffer[_buffer_index + 1] = timestamp;
        // _buffer_index = (_buffer_index + 2) % _buffer_size;
        memcpy(_large_buffer + _buffer_index, &size, sizeof(int));
        memcpy(_large_buffer + _buffer_index + sizeof(int), &timestamp, sizeof(double));
        _buffer_index = 
            (_buffer_index + (sizeof(int) + sizeof(double))) 
            % (_buffer_size * (sizeof(int) + sizeof(double)));

        // Might want to improve this to reduce the critical section
        if (_buffer_index == 0) {
            // These arrays should be de-allocated in the workers
            data.emplace_back(_large_buffer);
            _large_buffer = new char[ _buffer_size * (sizeof(int) + sizeof(double)) ];
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
    close(outputFile);
}

CLICK_ENDDECLS
ELEMENT_PROVIDES(ThreadPool)

