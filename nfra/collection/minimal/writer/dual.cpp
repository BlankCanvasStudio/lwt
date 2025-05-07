define (

    $PIPE_DPDK_PCI 0000:81:00.2,

    $INTERNET_DPDK_PCI 0000:81:00.3

)

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
dpdkIn :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 429496);
dpdkOut :: ToDPDKDevice($PIPE_DPDK_PCI);


internetIn :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 429496);
internetOut :: ToDPDKDevice($INTERNET_DPDK_PCI);

rec :: DataRecorder("data.csv", THREADS 16, BUFFER_SIZE 8196);

dpdkIn -> rec -> internetOut;
// internetIn -> DataRecorder("data.csv", THREADS 16, BUFFER_SIZE 4048) -> dpdkOut;
internetIn -> rec -> dpdkOut;
// internetIn -> DataRecorder("data.csv", THREADS 12, BUFFER_SIZE 4048) -> dpdkOut;//
// internetIn -> DataRecorder("data.csv", THREADS 12, BUFFER_SIZE 8196) -> dpdkOut;// internetIn -> dpdkOut;

