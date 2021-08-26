#!/usr/bin/python 
# -*- coding: utf-8 -*-
# import picamera
# import picamera_streaming

from lib.Motor import *
from lib.servo import *
# from Led import *
# from Buzzer import *
from lib.ADC import *
# from Thread import *
# from Light import *
from lib.Ultrasonic import *
# from Line_Tracking import *
# from threading import Timer
# from threading import Thread
# from Command import COMMAND as cmd
import queue
from threading import Thread

class SmartCar:
    def __init__(self):
        self.PWM=Motor()
        self.keypress_events_queue = queue.Queue()
        self.servo=Servo()
        # self.led=Led()
        self.ultrasonic=Ultrasonic()
        # self.buzzer=Buzzer()
        self.adc=Adc()
        # self.light=Light()
        # self.infrared=Line_Tracking()
        self.tcp_Flag = True
        self.sonic=False
        self.Light=False
        self.Mode = 'one'
        self.endChar='\n'
        self.intervalChar='#'

        self.PWM.setMotorModel(0, 0, 0, 0)
        self.servo.setServoPwm('0', 90)
        self.servo.setServoPwm('1', 90)

        Thread(target=self.process_keypress_queue).start()



    def process_keypress_queue(self):
        while True:
            keypressed = self.keypress_events_queue.get()
            if keypressed in ['a','s','w','d']:
                self.move(keypressed)
            elif keypressed in ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight']:
                self.look(keypressed)
            else:
                pass

    def flush_keypress_events(self):
        self.keypress_events_queue.queue.clear()

    def enqueue_keypress_event(self, keypress_event):
        self.keypress_events_queue.put(keypress_event)
    def Power(self):
        ADC_Power = self.adc.recvADC(2)*3
        # print ("Power:", ADC_Power)
        return ADC_Power
    def get_ultrasonic_distance(self):
        return self.ultrasonic.get_distance()

    def look(self, keypressed):
        print ("Keypressed:", keypressed)
        if keypressed == 'ArrowUp':
            self.servo.servo1_state = self.servo.servo1_state + 10
            if self.servo.servo1_state > 180:
                self.servo.servo1_state = 180

            self.servo.setServoPwm('1',self.servo.servo1_state)
        elif keypressed == 'ArrowDown':
            self.servo.servo1_state = self.servo.servo1_state - 10
            if self.servo.servo1_state < 80:
                self.servo.servo1_state = 80

            self.servo.setServoPwm('1',self.servo.servo1_state)
        elif keypressed == 'ArrowLeft':
            self.servo.servo0_state = self.servo.servo0_state - 10
            if self.servo.servo0_state < 0:
                self.servo.servo0_state = 0

            self.servo.setServoPwm('0',self.servo.servo0_state)
        elif keypressed == 'ArrowRight':
            self.servo.servo0_state = self.servo.servo0_state + 10
            if self.servo.servo0_state > 180:
                self.servo.servo0_state = 180

            self.servo.setServoPwm('0',self.servo.servo0_state)
        # else:
        #     pass

    def move(self, keypressed):
        print ("Keypressed:", keypressed)
        if keypressed == 's':
            self.PWM.setMotorModel(2000,2000,2000,2000)
        elif keypressed == 'w':
            self.PWM.setMotorModel(-2000,-2000,-2000,-2000)
        elif keypressed == 'd':
            self.PWM.setMotorModel(-500,-500,2000,2000)
        elif keypressed == 'a':
            self.PWM.setMotorModel(2000,2000,-500,-500)
        else:
            pass
        time.sleep(1)
        self.PWM.setMotorModel(0, 0, 0, 0)

if __name__=='__main__':
    pass
