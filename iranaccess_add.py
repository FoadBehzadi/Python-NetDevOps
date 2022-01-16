#add ip to iranaccess list using netmiko to connect to router
from unittest import result
from netmiko import ConnectHandler
from getpass import getpass
import ipaddress
import re
print("Iran Access, Be Careful!")
username = input("Enter UserName: ")
password = getpass("Enter PassWord: ")
address = str(input("Enter IP: "))
#Check if this is a valid IP address or not
try:
    ip = ipaddress.ip_address(address)
    print("IP address {} is valid. ".format(address, ip))
except ValueError:
    print("IP address {} is not valid ".format(address))
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
N5k_ssh = ConnectHandler(**N5k)
#Check if ip is ours or not! if it shows in routing table then its ours.
result_show_ip_route = N5k_ssh.send_command("show ip route  " + address)
matched = re.findall("Route not found",result_show_ip_route)
is_match = bool(matched)
if is_match:
    print("Be CareFull!!!! This IP Doesn't Belong To Us!")
    exit()
else:
    print("IP address", address ,"is ours :)")
    #fine Nexthop to add a static route for /32 subnet
    regex = r"\*via ([^;]*), \["
    nexthop = re.findall(regex,result_show_ip_route)
    #add static route
    config_ip_route = N5k_ssh.send_config_set("ip route " + address + "/32" + " " + str(nexthop[0]) + " name DYNAMIC-IRANACCESS")
    #add /32 to prefix-lists
    config_ip_prefixlist_RTBH = N5k_ssh.send_config_set("ip prefix-list RTBH permit " + address + "/32" )
    config_ip_prefixlist_Asiatech = N5k_ssh.send_config_set("ip prefix-list Asiatech-IDC-1 permit " + address + "/32" )
    #add /32 network to bgp 
    str_address = " " + address + "/32"
    config_add_bgp_network = [ 'router bgp 48715', 'address-family ipv4 unicast', 'network ' + str_address ]
    result_add_bgp_network = N5k_ssh.send_config_set(config_add_bgp_network)
#check if community route-map exists or not
result_N5k_rtbh_route_map_is_exist = N5k_ssh.send_command("show route-map RTBH")
matched_route_map_exist = re.findall("Policy RTBH not found", result_N5k_rtbh_route_map_is_exist)
#create route-map if it doesnt exist
if matched_route_map_exist:
    #set tag to bgp prefix
    print("creating route-map")
    config_create_route_map_seq10 = ['route-map RTBH permit 10', 'match ip address prefix-list RTBH', 'set community 43754:666']
    result_create_route_map_seq10 = N5k_ssh.send_config_set(config_create_route_map_seq10)
    config_create_route_map_seq100 = ['route-map RTBH permit 100']
    result_create_route_map_seq100 = N5k_ssh.send_config_set(config_create_route_map_seq100)
#check if route-map applyed on bgp    
result_N5k_rtbh_route_map_under_bgp_is_exist = N5k_ssh.send_command("sh ip bgp neighbors 172.24.125.9")
print(result_N5k_rtbh_route_map_under_bgp_is_exist)
matched_route_map_under_bgp = re.findall("Outbound route-map configured is RTBH", result_N5k_rtbh_route_map_under_bgp_is_exist)
is_match_route_map  = bool(matched_route_map_under_bgp)
if is_match_route_map:
    result_N5k_clear_ip_bgp = N5k_ssh.send_command("clear ip bgp 172.24.125.9 soft")
    print(result_N5k_clear_ip_bgp)
else:
    config_bgp_route_map = ['router bgp 48715', 'neighbor 172.24.125.9 remote-as 43754', 'address-family ipv4 unicast', 'route-map RTBH out', 'clear ip bgp 172.24.125.9 soft']
    result_bgp_route_map = N5k_ssh.send_config_set(config_bgp_route_map )
    print(result_bgp_route_map)
N5k_ssh.disconnect()
