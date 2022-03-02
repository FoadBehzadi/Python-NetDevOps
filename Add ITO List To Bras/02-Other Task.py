import json
import ipaddress
from ipaddress import IPv4Interface
from ipaddress import IPv4Address
from ipaddress import IPv4Network
from ipaddress import ip_network


import os #to use local system environment. on local system we did export export NET_TEXTFSM='/home/fup/textfsm/ntc-templates-master/ntc_templates/templates/'
# or alternativly we could add export NET_TEXTFSM=/home/fup/ito/ntc_templates/templates/ to end of ~/.bashrc
from dotenv import load_dotenv # its whrer we stored username and password||||it must install with pip3 install python-dotenv
from netmiko import ConnectHandler

load_dotenv()
username = os.environ.get('username')
password = os.environ.get('password')
secret = os.environ.get('secret')

#Device authentication info 
bras = {
    'device_type': 'cisco_ios',
    'host':   '192.168.1.2',
    'username': username,
    'password': password,
    'secret': secret, #anable secret
}

#convert Json to Dictionary
with open("/home/fup/ito/test.json") as handlee:
    itodict = json.load(handlee)
#parse Data List from Dictionary
DataList = itodict['Data']
mylist = []
for site in DataList:
    #print(site["ipv4"])
    xxx = site['ipv4']
    yyy = site['numberIpv4']
    itoip=(xxx,"/",yyy)   
    ipremovedspace = str(itoip).replace(" ","")
    ipremovedspace2 = str(ipremovedspace).replace("'","")
    ipremovedspace3 = str(ipremovedspace2).replace(",","")
    ipremovedspace4 = str(ipremovedspace3).replace("(","")
    ipremovedspace5 = str(ipremovedspace4).replace(")","")
    #print(str(ipremovedspace5))
    #print(ipremovedspace5)
    #interface = IPv4Interface('9.9.9.9/29')
    #print(interface.network)
    ipremovedspace6 = IPv4Interface(ipremovedspace5)
    mylist.append(IPv4Interface(ipremovedspace6.network))


without_duplicate = list(set(mylist))
'''for i in mylist:
    if i not in without_duplicate:
        without_duplicate.append(i)'''


'''print(without_duplicate[1])
print(type(without_duplicate[1]))
dup_index= without_duplicate.index("185.143.233.213/32")
print(dup_index)'''

list3 = []
for i in without_duplicate:
    list_temp = without_duplicate.copy()
    list_temp.remove(i)
    for k in list_temp:
        if ip_network(i).subnet_of(ip_network(k)):
            print(ip_network(i), " is subnet of ", ip_network(k))
            list3.append(i)
            

list3_without_duplicate = list(set(list3))
print("1111111111111111111111",without_duplicate)
for i in list3_without_duplicate:
    without_duplicate.remove(i)
print("2222222222222222222222",without_duplicate)


try:
    bras_ssh = ConnectHandler(**bras)
    #** means that extract bras dictionary here and use it as feed
    bras_ssh.enable() #use to enter enable secret
    show_result = bras_ssh.send_command('sh ip access-lists fup', use_textfsm=True)
    '''use_textfsm=True convert output to python dictionary
    show_result is a list of bunch of dictionary
    to do that we need to show where the ntc_templates is
    so we should import os and set the NET_TEXTFSM environment variable to point to the ./ntc-templates/templates'''
    #print(json.dumps(show_result, indent=2))
    #get the python dictionary and turn it into json and prettify it
    for entry in show_result:
        #if entry['acl_name'] == 'FUP' and entry['protocol'] == 'ip':
        #check if var is not Empty
        #if entry['dst_any'] :
        #if entry['dst_any'] !=None: 
        #check if var is Empty
        if entry["line_num"] != "":
            seq32 = entry['line_num']
            if entry["src_network"] == "":
                acl_ip = entry['src_host']+"/32"
            elif entry["src_host"] == "":
                bib = IPv4Address._prefix_from_ip_int(int(IPv4Address(entry['src_wildcard']))^(2**32-1))
                acl_ip = entry['src_network']+"/"+str(bib)


            if acl_ip in str(without_duplicate):
                dup_index= without_duplicate.index(acl_ip)
                print(acl_ip)
                print(dup_index)
            else:
                print(seq32," remove from bras")
                remove_acl_entry_from_bras = [ 'ip access-list extended fup', 'no  ' + seq32 ]
                result_remove_acl_entry_from_bras = bras_ssh.send_config_set(remove_acl_entry_from_bras)        





        #other way to do that
        #if interface['status'] == 'administratively down' or interface['status'] == 'down':     
            ##############################print(f"{entry['line_num']} is down!")
            # f means its formatted string and replace {interface['intf']} with its value
    bras_ssh.disconnect()
except Exception as error:
    print(error)    


bras_ssh.disconnect()
