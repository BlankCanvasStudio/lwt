c1 :: Classifier(12/0800, -);
c2 :: Classifier(12/0800, -);

out1 :: Queue(10000) -> LinkUnqueue(0ms, 10Gbps) -> ToDPDKDevice(0000:81:00.3);
out2 :: Queue(10000) -> LinkUnqueue(0ms, 10Gbps) -> ToDPDKDevice(0000:81:00.2);

c1[0] -> out1; //dr1 :: DataRecorder() -> out1;
c1[1] -> out1;
c2[0] -> dr1 :: DataRecorder() -> out2;
c2[1] -> out2;

FromDPDKDevice(0000:81:00.2, NUMA true, BURST 4) -> c1;
FromDPDKDevice(0000:81:00.3, NUMA true, BURST 4) -> c2;

