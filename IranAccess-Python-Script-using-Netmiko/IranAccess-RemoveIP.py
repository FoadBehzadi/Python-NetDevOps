#remove ip from iranaccess list using netmiko to connect to router
from netmiko import ConnectHandler
import ipaddress
import re
import sys
print("Remove ip from Iran Access list, Be Careful!")

username = sys.argv[1]
password = sys.argv[2]
address = sys.argv[3]

#Check if this is a valid IP address or not
try:
    ip = ipaddress.ip_address(address)
    print("IP address {} is in valid format ".format(address, ip))
except ValueError:
    print("IP address {} is not in valid format ".format(address))
    #Exit code if it is not in valid ip address format
    exit()
#Device authentication info 
N5k = {
    'device_type': 'cisco_ios',
    'host':   '192.168.240.1',
    'username': username,
    'password': password,
}
#connect to device
print("connecting to router ...")   
N5k_ssh = ConnectHandler(**N5k)
#Check if ip is ours or not! if it shows in routing table then its ours.
result_show_ip_route = N5k_ssh.send_command("show ip route  " + address + "/32")
matched_tag666 = re.findall("tag 666",result_show_ip_route)
is_match_tag666 = bool(matched_tag666)
if is_match_tag666:
    print("IP address", address ,"is in RTBH list")
    print("Removing IP route ", address , " ...")
    #find Nexthop to add a static route for /32 subnet
    regex = r"\*via ([^;]*), \["
    nexthop = re.findall(regex,result_show_ip_route)
    #add static route
    config_ip_route = N5k_ssh.send_config_set("no ip route " + address + "/32" + " " + str(nexthop[0]) )
else:
    print("Be CareFull!!!! IP address", address ,"is not in RTBH list ")
    exit()
result_prefixlist_entry_count = N5k_ssh.send_command("show ip prefix-list RTBH ")
matched_1entries = re.findall("RTBH: 1 entries",result_prefixlist_entry_count)
is_match_1entries = bool(matched_1entries)
if is_match_1entries:
    #bgp no route-map
    print( address, " is last entry in prefixlist")
    print("removing route-map in bgp neighbor ...")
    config_bgp_remove_route_map = ['router bgp 48715', 'neighbor 172.24.125.9 remote-as 43754', 'address-family ipv4 unicast', 'no route-map RTBH out', 'clear ip bgp 172.24.125.9 soft']
    result_bgp_remove_route_map = N5k_ssh.send_config_set(config_bgp_remove_route_map, delay_factor=4)
    #print(result_bgp_remove_route_map)
#bgp no network
str_address =  address + "/32"
print("remove ", address , " from bgp network ...")
config_bgp_remove_network = [ 'router bgp 48715', 'address-family ipv4 unicast', 'no network ' + str_address ]
result_bgp_remove_network = N5k_ssh.send_config_set(config_bgp_remove_network)
#print(result_bgp_remove_network)
print("clear bgp neighbor ...")
result_N5k_clear_ip_bgp = N5k_ssh.send_command("clear ip bgp 172.24.125.9 soft")
#remove /32 to prefix-lists
print("removing ", address, " from prefix list ...")
config_remove_ip_prefixlist_RTBH_entry = N5k_ssh.send_config_set("no ip prefix-list RTBH permit " + address + "/32")
config_remove_ip_prefixlist_Asiatech = N5k_ssh.send_config_set("no ip prefix-list Asiatech-IDC-1 permit " + address + "/32")
print("Saving Config ...")
config_write_memory = N5k_ssh.send_command("copy running-config startup-config ")
'''else:
    #bgp no network
    str_address = " " + address + "/32"
    print("remove ", address , " from bgp network ...")
    config_bgp_remove_network = [ 'router bgp 48715', 'address-family ipv4 unicast', 'no network ' + str_address, 'clear ip bgp 172.24.125.9 soft']
    result_bgp_remove_network = N5k_ssh.send_config_set(config_bgp_remove_network)
    print("clear bgp neighbor ...")
    #remove /32 to prefix-lists
    print("removing ", address, " from prefix list ...")
    config_remove_ip_prefixlist_RTBH_entry = N5k_ssh.send_config_set("no ip prefix-list RTBH permit " + address + "/32")
    config_remove_ip_prefixlist_Asiatech = N5k_ssh.send_config_set("no ip prefix-list Asiatech-IDC-1 permit " + address + "/32")
    print("Saving Config ...")
    config_write_memory = N5k_ssh.send_command("copy running-config startup-config ")'''

N5k_ssh.disconnect()


