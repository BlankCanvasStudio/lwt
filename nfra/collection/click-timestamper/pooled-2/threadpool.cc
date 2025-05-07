#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <vector>
#include <queue>
#include <memory>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <functional>
#include <stdexcept>
#include <string>

class ThreadPool {
    public:
        ThreadPool();
        ThreadPool(size_t, std::string filename);
        void enqueue(int size, float timestamp);
        ~ThreadPool();
    private:
        // need to keep track of threads so we can join them
        std::vector< std::thread > workers;
        // the data queue
        std::queue< int, float > data;

        // synchronization
        std::mutex queue_mutex;
        std::mutx file_mutex;
        std::condition_variable condition;

        // file writing materials
        void write_datapoint(int size, float timestamp);
        std::string _filename;
        std::ofstream outputFile;
        char colon = ':';
        char comma = ',';
        bool stop;
};

// the constructor just launches some amount of workers
inline ThreadPool::ThreadPool(size_t threads, std::string filename) : stop(false)
{
    _filename = filename;
    
    outputFile << std::fixed << std::setprecision(15);
    outputFile.open(filename.c_str(), std::ios::app | std::ios::binary);
    if (!outputFile) { click_chatter("Failed to open file"); }

    for(size_t i = 0;i<threads;++i)
        workers.emplace_back([this] {
            for(;;) {
                std::pair< int, float > data_point;
                
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
                    this->data.pop();
                }

                // Split the tuple and write it
                this->write_datapoint(data_point.first, 
                        data_point.second);
            }
        });
}


void ThreadPool::write_datapoint(int size, float time) {
    // Critical section to write the data to the file
    {
        file_mutex.lock();

        outputFile << std::to_string(size);
        outputFile.write(&colon, sizeof(char));
        outputFile << stmp;
        outputFile.write(&comma, sizeof(char));
        outputFile.close();

        file_mutx.unlock();
    }
}

// add new work item to the pool
void ThreadPool::enqueue(int size, float time) {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);

        // don't allow enqueueing after stopping the pool
        if(stop)
            throw std::runtime_error("enqueue on stopped ThreadPool");

        data.emplace(size, time);
    }
    condition.notify_one();
}

// the destructor joins all threads
inline ThreadPool::~ThreadPool()
{
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        stop = true;
    }
    condition.notify_all();
    for(std::thread &worker: workers)
        worker.join();
}

#endif
