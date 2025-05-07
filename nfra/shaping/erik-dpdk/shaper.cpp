
FromDPDKDevice(0000:81:00.2, NUMA true, BURST 4) -> 
    LinkUnqueue(0ms, 10Gbps) -> 
    ToDPDKDevice(0000:81:00.3);

FromDPDKDevice(0000:81:00.3, NUMA true, BURST 4) -> 
    LinkUnqueue(0ms, 10Gbps) -> 
    ToDPDKDevice(0000:81:00.2);

