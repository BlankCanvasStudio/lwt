define (
    // IP Address of the pipe reciever
    $pipe_ip 10.0.6.2, 


    // Network config for the pipercv side of router
    $DPDK_PORT 0,
    $ip_in 10.0.6.1,
    $mac_in 52:dc:28:b7:21:53,


    // Outward facing internet
    $ip_out 10.0.4.2,
    $mac_out 62:56:e5:a3:21:0a, 
    $intr_out eth2,

    $next_hop 10.0.1.1
)

// Set up all the interfaces
// Always call your recording object DataRecorder then this program
//   works between various compiles too
FromDPDKDevice($DPDK_PORT, MODE "none", PROMISC true) -> 
    dpdkIn :: DataRecorder("data.csv"); 
dpdkOut :: ToDPDKDevice($DPDK_PORT);

internetOut :: ToDevice($intr_out);
internetOutQueue :: Queue;
internetOutQueue -> internetOut;


// Create control socket to interface with
// ControlSocket(unix, /tmp/ClickRecordSocket);



// Classify incoming content into ARP queries, ARP responses, and rest
//     This is for data coming into the public interface
internet_class :: Classifier(12/0806 20/0001, 12/0806 20/0002, -);
FromDevice($intr_out) -> internet_class;


// Handle ARP request coming into eth2 (internet facing)
inInternetARP :: ARPResponder($ip_out/24 $ip_in/24 $mac_out);
// Print if theres an error
inInternetARP[1] -> Discard;

// ARP response coming into eth2 
outInternetARP :: ARPQuerier($ip_out, $mac_out); 
outInternetARP -> internetOutQueue;


// ARP adjusting for protected node
internalARP :: ARPQuerier($ip_in, $mac_in); 
// internalARP -> dpdkOut;

internalARP -> ip_classif :: Classifier(12/0800, -);
ip_classif[0] -> dt :: DecIPTTL;
ip_classif[1] -> dpdkOut;

dt[0] ->  head :: CheckIPHeader(OFFSET 14);
dt[1] -> Discard;

head[0] -> tcp_udp_class :: Classifier(23/06, 23/11, -); 
head[1] -> Print("IP header check failed") -> Discard;

tcp_udp_class[0] -> SetTCPChecksum -> tcpCheck :: CheckTCPHeader;
tcp_udp_class[1] -> SetUDPChecksum -> udpCheck :: CheckUDPHeader;
tcp_udp_class[2] -> dpdkOut;


udpCheck[0] -> dpdkOut;
udpCheck[1] -> Print("UDP check failed", MAXLENGTH 5120) -> Discard;

tcpCheck[0] -> dpdkOut;
tcpCheck[1] -> Print("TCP check failed", MAXLENGTH 5120) -> Discard;


internet_class[0] -> inInternetARP[0] -> internetOutQueue;
internet_class[1] -> [1]outInternetARP;
// This needs to be improved to handle proper reverse translation
internet_class[2] -> Strip(14) -> SetIPAddress($pipe_ip) -> [0]internalARP;


// Filter data coming from protected node (ie not gen internet)
//     We respond to ARP requests in a static way. Bad but not broken
dpdkIn -> c :: Classifier(12/0806 20/0001, 12/0806 20/0002, -);


// Manage ARP queries for DPDK interface
DPDK_ARP :: ARPResponder($ip_in $mac_in);

c[0] -> DPDK_ARP; // -> dpdkOut;
c[1] -> [1]internalARP;
// Absolutely awesome way to do IP address resolution
c[2] -> Strip(14) -> GetIPAddress(16) -> LinuxIPLookup($intr_out) -> [0]outInternetARP;

DPDK_ARP[0] -> dpdkOut;
DPDK_ARP[1] -> Discard;

