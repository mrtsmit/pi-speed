#!/usr/bin/env python  

import sys
import time
import subprocess
import RPi.GPIO as GPIO 

BIT0 = 3   
BIT1 = 5  
BIT2 = 24  
BIT3 = 26  

WAIT1 = 0.2		# used in display_1 and display_2
WAIT2 = 0.001	# used in display_3

segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]  #0~9  
pins = [11,12,13,15,16,18,22,7,3,5,24,26]  
bits = [BIT0, BIT1, BIT2, BIT3]  

def print_msg():  
	print 'Program is running...'  
	#print 'Please press Ctrl+C to end the program...'  

def digitalWriteByte(val):  
	GPIO.output(11, val & (0x01 << 0))  
	GPIO.output(12, val & (0x01 << 1))  
	GPIO.output(13, val & (0x01 << 2))  
	GPIO.output(15, val & (0x01 << 3))  
	GPIO.output(16, val & (0x01 << 4))  
	GPIO.output(18, val & (0x01 << 5))  
	GPIO.output(22, val & (0x01 << 6))  
	GPIO.output(7,  val & (0x01 << 7))  

def display_1():  
	GPIO.output(BIT0, GPIO.LOW)   
	for i in range(10):  
		digitalWriteByte(segCode[i])  
		time.sleep(WAIT1)  

def display_2():  
	for bit in bits:  
		GPIO.output(bit, GPIO.LOW)   
	for i in range(10):  
		digitalWriteByte(segCode[i])  
		time.sleep(WAIT1)  

def display_3(num):  
	b0 = num % 10  
	b1 = num % 100 / 10   
	b2 = num % 1000 / 100  
	b3 = num / 1000  
	if num < 10:  
		GPIO.output(BIT0, GPIO.LOW)   
		GPIO.output(BIT1, GPIO.HIGH)   
		GPIO.output(BIT2, GPIO.HIGH)   
		GPIO.output(BIT3, GPIO.HIGH)   
	 	digitalWriteByte(segCode[b0])  
	elif num >= 10 and num < 100:  
		GPIO.output(BIT0, GPIO.LOW)  
		digitalWriteByte(segCode[b0])  
		time.sleep(WAIT2)  
		GPIO.output(BIT0, GPIO.HIGH)   
		GPIO.output(BIT1, GPIO.LOW)  
		digitalWriteByte(segCode[b1])  
		time.sleep(WAIT2)  
	 	GPIO.output(BIT1, GPIO.HIGH)
		GPIO.output(BIT2, GPIO.HIGH)   
		GPIO.output(BIT3, GPIO.HIGH)
	elif num >= 100 and num < 1000:  
		GPIO.output(BIT0, GPIO.LOW)  
		digitalWriteByte(segCode[b0])  
		time.sleep(WAIT2)  
		GPIO.output(BIT0, GPIO.HIGH)   
		GPIO.output(BIT1, GPIO.LOW)  
		digitalWriteByte(segCode[b1])  
		time.sleep(WAIT2)  
		GPIO.output(BIT1, GPIO.HIGH)  
		GPIO.output(BIT2, GPIO.LOW)  
		digitalWriteByte(segCode[b2])  
		time.sleep(WAIT2)  
	 	GPIO.output(BIT2, GPIO.HIGH)
		GPIO.output(BIT3, GPIO.HIGH)
	elif num >= 1000 and num < 10000:  
		GPIO.output(BIT0, GPIO.LOW)  
		digitalWriteByte(segCode[b0])  
		time.sleep(WAIT2)  
		GPIO.output(BIT0, GPIO.HIGH)   
		GPIO.output(BIT1, GPIO.LOW)  
		digitalWriteByte(segCode[b1])  
		time.sleep(WAIT2)  
		GPIO.output(BIT1, GPIO.HIGH)  
		GPIO.output(BIT2, GPIO.LOW)  
		digitalWriteByte(segCode[b2])  
		time.sleep(WAIT2)  
		GPIO.output(BIT2, GPIO.HIGH)   
		GPIO.output(BIT3, GPIO.LOW)  
		digitalWriteByte(segCode[b3])  
		time.sleep(WAIT2)  
	 	GPIO.output(BIT3, GPIO.HIGH)   
	else:  
		 print 'Out of range, num should be 0~9999 !'  

def setup():  
	GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location  
	GPIO.setwarnings(False)
	for pin in pins:  
		GPIO.setup(pin, GPIO.OUT)    #set all pins' mode is output  
		GPIO.output(pin, GPIO.HIGH)  #set all pins are high level(3.3V)  
	display_1()
	display_2()

def loop():  
	while True:
		for pin in pins:
			GPIO.output(pin, GPIO.LOW)  
		# MEASURING LED on
		downspeed = 0
		print "Measuring download speed ..."
		try:
			downspeed = int(subprocess.check_output([sys.executable, "collect.py"]))
		except:
			print "Something went wrong ..."
			downspeed = 0
			pass
		print downspeed
		# MEASURING LED off
		for i in range(264000): # about every 15 minutes, with "WAIT2 = 0.001"
#		for i in range(4000): # quick, about every 30 seconds
			display_3(downspeed)  

def destroy():   #When program ending, the function is executed.   
	for pin in pins:    
		GPIO.output(pin, GPIO.LOW) #set all pins are low level(0V)   
		GPIO.setup(pin, GPIO.IN)   #set all pins' mode is input  

if __name__ == '__main__': #Program starting from here   
	setup()
	print "Initializing ....."
	try:  
		loop()    
	except KeyboardInterrupt:    
		destroy()    
