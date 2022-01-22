from netmiko import ConnectHandler
import re
import sys
username = sys.argv[1]
password = sys.argv[2]

N5k = {
    'device_type': 'cisco_ios',
    'host':   '192.168.240.1',
    'username': username,
    'password': password,
}
#connect to device
#print("connecting to router ...")     
N5k_ssh = ConnectHandler(**N5k)

result_show_ip_prefix_list = N5k_ssh.send_command("show ip prefix-list RTBH  " )
#print(result_show_ip_prefix_list)
regex = r"(?<=permit).*"
nexthop = re.findall(regex,result_show_ip_prefix_list)
#print(nexthop)
for ip in nexthop:
    print(ip)
