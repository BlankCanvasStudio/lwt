define (

    $PIPE_DPDK_PCI 0000:81:00.2,

    $INTERNET_DPDK_PCI 0000:81:00.3

)

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
dpdkIn :: FromDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 429496);
dpdkOut :: ToDevice($PIPE_DPDK_PCI);


internetIn :: FromDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 429496);
internetOut :: ToDevice($INTERNET_DPDK_PCI);


dpdkIn ->  internetOut;
// internetIn -> DataRecorder("data.csv") -> dpdkOut;
 internetIn -> dpdkOut;

