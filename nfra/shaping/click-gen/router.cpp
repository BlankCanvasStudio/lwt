define (

    $PIPE_DPDK_PCI 0000:81:00.3,

    $INTERNET_DPDK_PCI 0000:81:00.2,

)


dpdkIn      :: FromDPDKDevice($PIPE_DPDK_PCI, SCALE PARALLEL, NUMA true);
dpdkOut     :: ToDPDKDevice($PIPE_DPDK_PCI);


internetIn  :: FromDPDKDevice($INTERNET_DPDK_PCI, SCALE PARALLEL, NUMA true);
// Try just slightly higher
internetOut :: Queue(1000000) -> LinkUnqueue(0ns, 100001000bps) -> ToDPDKDevice($INTERNET_DPDK_PCI);


dpdkIn ->  internetOut;
internetIn -> dpdkOut;

