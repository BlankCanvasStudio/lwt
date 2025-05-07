define (

    $PIPE_DPDK_PCI 0000:81:00.2,

    $INTERNET_DPDK_PCI 0000:81:00.3

)

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
dpdkIn :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true, BURST 4);
dpdkOut :: Queue(10000) -> LinkUnqueue(0ms, 10Gbps) -> ToDPDKDevice($PIPE_DPDK_PCI);


internetIn :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true, BURST 4);
internetOut :: Queue(10000) -> LinkUnqueue(0ms, 10Gbps) -> ToDPDKDevice($INTERNET_DPDK_PCI);


dpdkIn ->  internetOut;
internetIn -> DataRecorder("data.csv", BUFFER_SIZE 256) -> dpdkOut;

