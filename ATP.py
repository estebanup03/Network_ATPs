#!/usr/bin/env python3
import os
from netmiko import ConnectHandler
import os
import sys
import time
import getpass

#DATA

# Define the log file name format
timestr = time.strftime("%Y%m%d_%H%M%S")


Device = input("Ingrese vendor de equipo:\n1. Cisco\n2. Juniper\n")
IP = input("Ingrese la IP del equipo: ")

#IP = "IP"
user = "user"
password = "password"
#password = getpass.getpass()

juniper_junos = {
    'device_type': 'juniper',
    'ip': IP,
    'username': user,
    'password': password,
}
cisco = {
    'device_type': 'cisco_ios',
    'host': IP,
    'username': user,
    'password': password,
}

def get_hostname_junos(sesion):
    # global_delay_factor IS THE KEY
    output = sesion.send_command('show configuration | display set | match host-name')
    hostname = output.replace('set system host-name ', '')
    print("Obteniendo Hostname...\n")
    return hostname

def get_config_junos(sesion):
    output = sesion.send_command('show configuration | display set')
    print("Obteniendo Configuracion...\n")
    return output

def get_hostname_ciscoios(sesion):
    output = sesion.send_command('show run | inc hostname')
    hostname = output.replace('hostname ', '')
    print("Obteniendo Hostname...\n")
    return hostname

def get_config_ciscoios(sesion):
    output = sesion.send_command('terminal length 0')
    print(output)
    output = sesion.send_command('show run')
    print("Obteniendo Configuracion...\n")
    return output


def save_to_file(name_file,text):
    with open(name_file , 'w') as f:
        print(text, file=f)

########################################################################################################################
# Open the log file


if Device == '2':
    deviceSub = input("Ingrese tipo de equipo:\n1. SRX\n2. EX\n")
    if deviceSub == '1':
        commands = open('ATP_Juniper_SRX.txt')
    else:
        commands = open('ATP_Juniper_EX.txt')    
    net_connect = ConnectHandler(**juniper_junos, global_delay_factor=2)
    print("¡Conexión exitosa!")
    hostname = get_hostname_junos(net_connect)
    print(hostname)
    hostname = hostname.strip("\n")
    new_hostname = hostname.replace(".", "_")
    config = get_config_junos(net_connect)
    save_to_file("BCK_" + new_hostname + ".txt", config)
    print("Guardando backup...\n")
    outputfile = 'ATP_'+new_hostname + timestr + '.txt'
    log = open(outputfile, 'a')
    for line in commands:
        output = net_connect.send_command(line, strip_command=False)
        print("Completando ATP:" + line)
        print(output, file=log)
        print("*" * 64, file=log)
        print(" ", file=log)
    commands.close()
else:
    commands = open('ATP_Cisco.txt')
    net_connect = ConnectHandler(**cisco, global_delay_factor=2)
    hostname = get_hostname_ciscoios(net_connect)
    print(hostname)
    hostname = hostname.strip("\n")
    new_hostname = hostname.replace(".", "_")
    config = get_config_ciscoios(net_connect)
    save_to_file("BCK_" + new_hostname + ".txt", config)
    print("Guardando backup...\n")
    outputfile = 'ATP_'+new_hostname + timestr + '.txt'
    log = open(outputfile, 'a')
    for line in commands:
        output = net_connect.send_command(line, strip_command=False)
        print(output, file=log)
        print("*" * 64, file=log)
        print(" ", file=log)
    commands.close()
