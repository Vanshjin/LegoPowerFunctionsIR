#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
legopfpin = 7

message = [False,True,False,False, False,False,False,False, False,False,False,False, False,False,False,False]
stdchannel = 0
#truelen = 

class pf(object):
	def __init__(self,pin,channel = 0):
		#print 'Hi, this is mymodule speaking.'
		#print pin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		legopfpin = pin
		stdchannel = channel
	def blink(self):
		#GPIO.output(legopfpin,True)
		#time.sleep(1)
		GPIO.output(legopfpin,False)
		time.sleep(1)
		GPIO.output(legopfpin,True)
	def hello(self):
		print 'hello'
		print legopfpin
	def single_pwm_out(self,channel=stdchannel,side=0,mode=3,step=1):
		#print hello
		if channel > 3 or channel < 0:
			print "channel must 0-3"
			return
		if side=="red":
			side = 0 # ich hoffe es. Muss ich noch ausprobieren
		if side=="blue":
			side = 1
		if not (side ==1 or side ==0):
			print "side must 0 or 1"
			return
		if mode=="for":
			mode = 0
		if mode=="bck":
			mode = 1
		if mode=="brk":
			mode = 2
		if mode=="flo":
			mode = 3
		if mode not in [0,1,2,3]:
			print "mode must be 0-3 or for,bck,brk,flo"
			return
		if step not in [1,2,3,4,5,6,7]:
			print "step must be 1-7"
			return
		for i in range(12):
			message[i] = False
		message[0] = False #toggel dosent matter
		message[1] = False #escape
		if channel == 2 or channel == 3:
			message[2] = True
		if channel == 1 or channel == 3:
			message[3] = True
		message[4] = False #adress
		message[5] = True#mode
		message[6] = False#mode
		message[7] = False#mode
		
		if mode == 2:
			message[8:12] = [True,False,False,False]
		elif mode == 3:
			message[8:12] = [True,False,False,False]
		elif mode == 0 or mode == 1:
			i = 0
			
			if mode == 1:
				i+=8
				step = (step-1)*-1+7
			i +=step
		message[8:12] = self._num_array(i)
		self._checksum()
		self.send()
	def _checksum(self):
		for i in range(4):
			message[i+12] = (((True != message[i]) != message[i+4]) != message[i+8])
		#print message
	#def __exit__(self):
		#print "ende"
		#GPIO.cleanup()
	def _num_array(self,number):
		array = [False,False,False,False]
		
		j=0
		for i in range(3,-1,-1):
			if number>=2**i:
				array[j] = True
				number-=2**i
				j+=1
		return array
		
	def get_message(self):
		print message
	def send(self):
		sendnumber =0;
		for i in range(16):
			if message[i]:
				sendnumber += 2**(i*-1+16)
		print sendnumber
		print os.system("sudo ./test " + str(legopfpin) + " " + str(sendnumber));
	def end(self):
		GPIO.cleanup()
		exit()

	
		

version = '0.1'

# End of mymodule.py