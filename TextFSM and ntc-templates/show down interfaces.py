import os #to use local system environment. on local system we did export export NET_TEXTFSM='/home/fup/textfsm/ntc-templates-master/ntc_templates/templates/'
from dotenv import load_dotenv # its whrer we stored username and password
from netmiko import ConnectHandler
import json

load_dotenv()
username = os.environ.get('username')
password = os.environ.get('password')
secret = os.environ.get('secret')

#Device authentication info  
bras = {
    'device_type': 'cisco_ios',
    'host':   '192.168.1.3',
    'username': username,
    'password': password,
    'secret': secret, #anable secret
}

try:
    bras_ssh = ConnectHandler(**bras)
    #** means that extract bras dictionary here and use it as feed
    bras_ssh.enable() #use to enter enable secret
    show_result = bras_ssh.send_command('show ip interface brief', use_textfsm=True)
    '''use_textfsm=True convert output to python dictionary
    to do that we need to show where the ntc_templates is
    so we should import os and set the NET_TEXTFSM environment variable to point to the ./ntc-templates/templates'''
    print(json.dumps(show_result, indent=2))
    #get the python dictionary and turn it into json and prettify it
    for interface in show_result:
        if interface['status'] == 'down':
            print(f"{interface['intf']} is down!")
    bras_ssh.disconnect()
except Exception as error:
    print(error)    
    '''
    includes all types of error like ZeroDivisionError and ValueError
    other method
    except ZeroDivisionError as error:
    print(error)
    except ValueError as error:
    print(error)
    ####or
    except (ZeroDivisionError, ValueError) as error:
    print(error)
    '''
