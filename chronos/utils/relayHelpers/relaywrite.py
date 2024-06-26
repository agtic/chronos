#!/usr/bin/python

#License
#-------
#This code is published and shared by Numato Systems Pvt Ltd under GNU LGPL 
#license with the hope that it may be useful. Read complete license at 
#http://www.gnu.org/licenses/lgpl.html or write to Free Software Foundation,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

#Simplicity and understandability is the primary philosophy followed while
#writing this code. Sometimes at the expence of standard coding practices and
#best practices. It is your responsibility to independantly assess and implement
#coding practices that will satisfy safety and security necessary for your final
#application.

#This demo code demonstrates how to read the status of a relay

import sys
import serial

if (len(sys.argv) < 2):
	print("Usage: relaywrite.py <RELAYNUM> <CMD>\nEg: relaywrite.py 0 on")
	sys.exit(0)
else:
	relayNum = sys.argv[1];
	relayCmd = sys.argv[2];

portName="/dev/ttyACM0"
#relayNum = 8
#Open port for communication
serPort = serial.Serial(portName, 19200, timeout=1)

#Send the command
serPort.write("relay "+ str(relayCmd) +" "+ str(relayNum) + "\n\r")
#serPort.write("relay off "+ str(relayNum) + "\n\r")
#

print("Command sent...")

response = serPort.read(25)

#print response

if(response.find("on") > 0):
	print("Relay " + str(relayNum) +" is ON")

elif(response.find("off") > 0):
	print("Relay " + str(relayNum) +" is OFF")

#Close the port
serPort.close()


