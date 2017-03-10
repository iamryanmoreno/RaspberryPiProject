"""
00  S  Line Speed  N13:2
01  S  Average Line Speed This Shift  N12:44
02  L  Lineal Remaining  N13:25-26
03  L  Lineal This Shift  N12:42
04  S  Average Line Speed This Day  N12:48
05  L  Wet End Lineal Remaining (calc.from sq.)
06  S  Single Facer 1 Speed
07  S  Total Downtime This Shift  N12:65
"""

import datetime
import os
import threading
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.clock import Clock
from base import Base
import serial
from kivy.uix.screenmanager import ScreenManager, Screen

class MainApp(App, Base):

    root = ObjectProperty(None)
    ser = ObjectProperty(None)

    def build(self):
        Base.__init__(self)
        #self.root = Builder.load_file('/home/pi/parse_serial/main_0.kv')
        self.root = Builder.load_file('main_0.kv')
        try:
            self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=1200, timeout=5)
            #self.ser = serial.Serial(port='COM9', baudrate=1200, timeout=5)
        except serial.SerialException as e:
            print e, ' Please check connection now.'

        #Clock.schedule_interval(self.display_datetime, 1)
        Clock.schedule_interval(self.display_datetime,2)
        threading.Thread(target=self.update_data).start()

    def display_datetime(self, *args):
        #time_now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        date_now = datetime.datetime.now().strftime('%a %d %b %Y')
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        self.root.ids['lb_date'].text = date_now
        self.root.ids['lb_time'].text = time_now

    def update_data(self, *args):
        """
        Update content periodically.
        :param args:
        :return:
        """
        line_num = 0
        if self.debug:
            f = open(self.cur_dir + 'sample.txt', 'r')
            lines = f.readlines()

        while True:
            if self.debug:
                if line_num == len(lines) - 1:
                    line_num = 0
                else:
                    line_num += 1
                data = lines[line_num][:-1]     # remove carriage return
                print "Line number: ", line_num
            else:
                data = ''
                # Read from STX to ETX
                # Sample: '[02]01 124[03]'
                while True:
                    try:
                        buf = self.ser.read()
                        if buf.encode('hex') == '02':
                            print "Found STX... "
                            data = '[02]'
                            while True:
                                tmp = self.ser.read()
                                if tmp.encode('hex') == '03':
                                    data += '[03]'
                                    break
                                else:
                                    data += tmp
                            break
                        else:
                            print 'Finding STX... ', buf.encode('hex')
                    except serial.SerialException as e:
                        print e
                        break

            #print data

            #if not data.startswith("[02") or not data.endswith("[03]"):
             #   print 'Invalid type of data.'
              #  print data
            if data.startswith('[02]'):
                #print "Found: ", data
                data_header = data[4:6]
                # data_list = ['00', '01', '02', '03', '04', '05', '06', '07']
                data_list = ['00', '02']
                if data_header in data_list:
                    content = data[7:-5]
                    tmp = '[b][color=FFEC1F]' + content + '[/color][/b]'
                    print "Updating content: ", data_header, tmp
                    self.root.ids['lb_' + data_header].text = tmp
                #else:
                 #   print "Invalid data header"
            time.sleep(.5)


if __name__ == '__main__':
    app = MainApp()
    app.run()
