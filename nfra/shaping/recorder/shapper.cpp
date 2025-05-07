define (

    $click_gen_interface 0000:81:00.3, // ens1f3,
    $click_gen_interface_ip 10.0.1.1,
    // $click_gen_ip 10.0.1.2,
    $click_gen_ip 10.0.0.1,

    $tap_usr_interface 0000:81:00.2, //ens1f2,
    $tap_usr_interface_ip 10.0.2.1,
    $tap_usr_ip 10.0.2.2,

    $router_two_interface 0000:81:00.1, //ens1f1,
    $router_two_interface_ip 10.0.3.1,
    $router_two_ip 10.0.3.2,

    $mac 62:56:e5:a3:21:0a,

)


click_gen_arpQ :: ARPQuerier($click_gen_interface_ip, $mac);
tap_usr_arpQ :: ARPQuerier($tap_usr_interface_ip, $mac);
limited_link_arpQ :: ARPQuerier($router_two_interface_ip, $mac);

// click_gen_arpQ_class :: Classifier(12/0800, -);
// tap_usr_arpQ_class :: Classifier(12/0800, -);
// limited_link_arpQ_class :: Classifier(12/0800, -);

// These need to ge fixed
click_gen_arpR :: ARPResponder($click_gen_interface_ip $mac);
tap_usr_arpR :: ARPResponder($tap_usr_interface_ip $mac);
limited_link_arpR :: ARPResponder($router_two_interface_ip $mac);

// Classify traffic into ARP requests, ARP responses, and rest
click_gen_class :: Classifier(12/0806 20/0001, 12/0806 20/0002, -);
tap_usr_class :: Classifier(12/0806 20/0001, 12/0806 20/0002, -);
limited_link_class:: Classifier(12/0806 20/0001, 12/0806 20/0002, -);



FromDPDKDevice($click_gen_interface, SCALE PARALLEL, NUMA true) -> 
    click_gen_class; 
FromDPDKDevice($tap_usr_interface, SCALE PARALLEL, NUMA true) -> 
    tap_usr_class; 
FromDPDKDevice($router_two_interface, SCALE PARALLEL, NUMA true) -> 
    limited_link_class;


to_click_gen :: ToDPDKDevice($click_gen_interface);
to_tap_usr :: ToDPDKDevice($tap_usr_interface);
// Implement limited link different since combining streams from 2 src
to_limited_link :: Queue(1000000) -> LinkUnqueue(0ns, 100000000bps) -> DataRecorder("data.csv") -> ToDPDKDevice($router_two_interface);

// Classify router_two IP traffic based on destination IP`
router_two_IP_class :: Classifier(30/0a000001, 30/0a000202, -);



// Respond to ARPs coming in on the interface
click_gen_class[0] -> click_gen_arpR[0] -> to_click_gen;
tap_usr_class[0] -> tap_usr_arpR[0] -> to_tap_usr;
limited_link_class[0] -> limited_link_arpR[0] -> to_limited_link;

// Log arps coming in on the interfaces
click_gen_class[1] -> [1]click_gen_arpQ;
tap_usr_class[1] -> [1]tap_usr_arpQ;
limited_link_class[1] -> [1]limited_link_arpQ;

// Sift through general traffic and update the IPs
// First update the IP and senf it through ARP reversal
// All traffic in from click_gen is to router_two
click_gen_class[2] -> Strip(14) -> SetIPAddress($router_two_ip) -> 
        [0]limited_link_arpQ;
// All traffic in from tap user is through router_two
tap_usr_class[2] -> Strip(14) -> SetIPAddress($router_two_ip) -> 
        [0]limited_link_arpQ;
// Filter traffic from router two based on its destination
limited_link_class[2] ->  router_two_IP_class;


// Send back to click gen
router_two_IP_class[0] -> Strip(14) -> SetIPAddress($click_gen_ip) ->
    [0]click_gen_arpQ;
// Send back to tap user
router_two_IP_class[1] ->  Strip(14) -> SetIPAddress($tap_usr_ip) ->
    [0]tap_usr_arpQ;
// Discard cause neither above
router_two_IP_class[2] -> Discard;


// Set up arpQ so that they update IPs, headers, checksums, etc

// Forward the arpQs to the classifiers:
click_gen_arpQ[0] -> to_click_gen; // click_gen_arpQ_class;
tap_usr_arpQ[0] -> to_tap_usr; // tap_usr_arpQ_class;
limited_link_arpQ[0] -> to_limited_link; // limited_link_arpQ_class;

// Classify incoming packets on if they are IP or not
// Send down decrement TTL path if yes, send straight through if not
/*
click_gen_arpQ_class[0] -> to_click_gen; // click_gen_dttl :: DecIPTTL;
click_gen_arpQ_class[1] -> to_click_gen;

tap_usr_arpQ_class[0] -> to_tap_usr; // tap_usr_dttl :: DecIPTTL;
tap_usr_arpQ_class[1] -> to_tap_usr;

limited_link_arpQ_class[0] -> to_limited_link; // limited_link_dttl :: DecIPTTL;
limited_link_arpQ_class[1] -> to_limited_link;
*/

