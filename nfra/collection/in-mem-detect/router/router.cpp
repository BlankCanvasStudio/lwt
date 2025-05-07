define (

    $PIPE_DPDK_PCI 0000:81:00.2,

    $INTERNET_DPDK_PCI 0000:81:00.3

)

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
dpdkIn :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 829496);
dpdkOut :: ToDPDKDevice($PIPE_DPDK_PCI);


internetIn :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 829496);
internetOut :: ToDPDKDevice($INTERNET_DPDK_PCI);


dpdkIn ->  internetOut;
internetIn -> MemoryDetector(SIZE 32768) -> dpdkOut;
// internetIn -> dpdkOut;

