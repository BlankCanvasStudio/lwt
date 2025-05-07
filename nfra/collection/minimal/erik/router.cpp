define (

    $PIPE_DPDK_PCI 0000:81:00.2,

    $INTERNET_DPDK_PCI 0000:81:00.3

)

ControlSocket(unix, /tmp/clicksocket);

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
// dpdkIn :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 429496);
dpdkIn :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true);
dpdkOut :: Queue(100000) -> LinkUnqueue(0ms, 10Gbps) -> ToDPDKDevice($PIPE_DPDK_PCI);


// internetIn :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true, MAXTHREADS 204800, BURST 429496);
internetIn :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true);
internetOut :: Queue(100000) -> LinkUnqueue(0ms, 10Gbps) -> ToDPDKDevice($INTERNET_DPDK_PCI);


dpdkIn ->  internetOut;

// 100 * 1000^2 bps
internetIn -> data :: DataRecorder("data.csv", THREADS 4, BUFFER_SIZE 512) -> dpdkOut;

// internetIn -> DataRecorder("data.csv", THREADS 2, BUFFER_SIZE 512) -> dpdkOut;

