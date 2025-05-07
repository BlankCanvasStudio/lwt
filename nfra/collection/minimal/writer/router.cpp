define (

    $PIPE_DPDK_PCI 0000:81:00.2,

    $INTERNET_DPDK_PCI 0000:81:00.3

)

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
dpdkIn :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true);
dpdkOut :: ToDPDKDevice($PIPE_DPDK_PCI);


internetIn :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true, BURST 4);
internetOut :: ToDPDKDevice($INTERNET_DPDK_PCI);


dpdkIn ->  internetOut;
internetIn -> DataRecorder("data.csv", THREADS 4, BUFFER_SIZE 512) -> dpdkOut;
// internetIn -> DataRecorder("data.csv", THREADS 16, BUFFER_SIZE 4048) -> dpdkOut;
// internetIn -> DataRecorder("data.csv", THREADS 16, BUFFER_SIZE 8196) -> dpdkOut;
// internetIn -> DataRecorder("data.csv", THREADS 12, BUFFER_SIZE 4048) -> dpdkOut;//
// internetIn -> DataRecorder("data.csv", THREADS 12, BUFFER_SIZE 8196) -> dpdkOut;// internetIn -> dpdkOut;

