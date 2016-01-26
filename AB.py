#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import time
import string
import threading
import shelve


ser = serial.Serial('/dev/ttyUSB0', 115200, 8, 'N', 1, timeout = 0.1)  # 配置串口
ser2 = serial.Serial('/dev/ttyUSB2', 9600, 8, 'E', 1, timeout = 0.1)
if ser2.isOpen() == False:
      ser2.open()
if ser.isOpen() == False:
      ser.open()
ser2.flush()
ser.flush()
pan_list = {'b': '1', 'c': '1', 'd': '1'}
SPORT = ['*', '2', 'A', '1', chr(0x2C), 'W', 'L', '5', 'A', chr(0x0D)]  # 通用串口云台控制
tan = ['*2V', '1', ',', '1', chr(0x0D)]
count = int(0)
CAMt = '1'
MONt = '1'
flag = 0
flag2 = 0
data = ''
pan = ''
stop = 'NG'
count = int(0)
count2 = int(0)

dict2 = {}
count3 = int(0)

try:
      db = shelve.open('tantt', 'c')
      for k in db.keys():
            tan[1] = db[k]
            tan[3] = k
            for i in range(0, 5):
                  ser2.write(tan[i])
            print tan
      db.close()
except:
      pass


def say ():  # 存储正在操作摄像头
      global count3
      global dict2
      global stop
      global pan_list
      pan_list.update()
      # print pan_list
      if stop != 'NG':
            if pan_list[stop] in dict2.keys():
                  dict2[pan_list[stop]] = int(0)
            if pan_list[stop] not in dict2.keys():
                  dict2[pan_list[stop]] = int(0)
      for i in dict2.keys():
            dict2[i] = dict2[i] + int(1)
            # print "dict2[%s] = %s" % (i,dict2[i])
            # print dict2
      for i in dict2.keys():
            # print "i=%s" % i
            if dict2[i] > 10:
                  dd = i
                  print "dd=%s" % dd
                  #  print 'send stop'
                  SPORT[6] = 'H'
                  c = string.atoi(i, 10)
                  if c % 16 == 0:
                        SPORT[3] = str(c / 16)
                        SPORT[8] = 'P'
                        for i in range(0, 10):
                              ser2.write(SPORT[i])
                              # for i in range(0,10):
                              #    ser2.write(SPORT[i])
                  else:
                        SPORT[3] = str((c / 16) + 1)
                        if c % 16 == 10:
                              SPORT[8] = 'J'
                        elif c % 16 == 11:
                              SPORT[8] = 'K'
                        elif c % 16 == 12:
                              SPORT[8] = 'L'
                        elif c % 16 == 13:
                              SPORT[8] = 'M'
                        elif c % 16 == 14:
                              SPORT[8] = 'N'
                        elif c % 16 == 15:
                              SPORT[8] = 'O'
                        else:
                              SPORT[8] = chr(ord(str(c % 16)) + 16)
                        SPORT[7] = '2'
                        for i in range(0, 10):
                              ser2.write(SPORT[i])
                  for i in range(0, 10):
                        ser2.write(SPORT[i])
                  print '%s' % SPORT
                  del dict2[dd]
      # count3 = count3+1
      global t
      #t = threading.Timer(0.005,say)
      #t.start()


if __name__ == "__main__":
      while True:
            try:
                  t = threading.Timer(0.005, say)  # 监测存储需要停止摄像头号
                  t.start()
                  t.join()

                  head = ser.read(1)
                  if head == '':
                        stop = 'NG'
                  if count != 0:
                        data = data + head
                        flag2 = 0
                  if head == ';':
                        data = data + head
                        count = count + 1
                        flag2 = 0
                  if head == '#':
                        count = 0
                        flag2 = 0
                        flag = 1
                  if flag == 1:
                        flag = 0
                        if 'a' in data:  # 开始处理指令
                              print "data = %s" % data
                              if 'M' in data and 'a' in data and '#' in data:
                                    MONt = data[(data.index('a') + 1): data.index('M')]
                                    if MONt == '':
                                          MONt = '1'
                                    print MONt
                                    CAMt = data[(data.index('M') + 2): data.index('#')]
                                    if CAMt == '':
                                          CAMt = '1'
                                    print CAMt
                              db = shelve.open('tantt', 'c')
                              db[MONt] = CAMt
                              db.close()
                              yy = '*2V'
                              yy = yy + MONt + ',' + CAMt + chr(0x0D)
                              print yy
                              ser2.write(yy)
                              if CAMt == pan_list['b'] or CAMt == pan_list['c'] or CAMt == ['d']:
                                    flag2 = 1
                                    count2 = 0
                                    pan = ''
                              else:
                                    flag2 = 0
                              data = ''
                        if 'a' not in data:
                              print "nodata = %s" % data
                              if 'M' in data and '#' in data:
                                    if len(data) < 10:
                                          pan_list[data[data.index('M') + 1]] = data[(data.index('M') + 2): data.index('#')]
                                          # print "pan_list[b]=%s" % pan_list['b']
                                          # print "pan_list[c]=%s" % pan_list['c']
                                          # print "pan_list[d] =%s" % pan_list['d']
                              pan = ''
                              flag2 = 1
                              count2 = 0
                        data = ''
                        # print 'flag2= %s' % flag2
                  if flag2 == 1 and head != '#':
                        count2 = count2 + 1
                        # print count2
                        if count2 > 1:
                              if count2 > 1000:
                                    count2 = 1
                              pan = pan + head
                              if len(pan) == 2:
                                    # stop = pan[1]
                                    # print "stop = %s pan[1] =%s" %  (stop,pan[1])
                                    if 'W' in pan:  # out
                                          if pan[1] == 'b' or pan[1] == 'c' or pan[1] == 'd':
                                                stop = pan[1]
                                          if pan[1] == '':
                                                pan[1] = 'b'
                                                # print "stop = %s pan[1] =%s" %  (stop,pan[1])
                                          SPORT[6] = 'O'
                                          # print "pan[1]=%s" % pan[1]
                                          # print "pan_list[]=%s" % pan_list[pan[1]]
                                          CAMR = pan_list.get(pan[1], '1')
                                          if CAMR == '':
                                                CAMR = '1'
                                                # print "CAMR=%s" % CAMR
                                          c = string.atoi(str(CAMR), 10)
                                          if c % 16 == 0:
                                                SPORT[3] = str(c / 16)
                                                SPORT[8] = 'P'
                                          else:
                                                SPORT[3] = str((c / 16) + 1)
                                                if c % 16 == 10:
                                                      SPORT[8] = 'J'
                                                elif c % 16 == 11:
                                                      SPORT[8] = 'K'
                                                elif c % 16 == 12:
                                                      SPORT[8] = 'L'
                                                elif c % 16 == 13:
                                                      SPORT[8] = 'M'
                                                elif c % 16 == 14:
                                                      SPORT[8] = 'N'
                                                elif c % 16 == 15:
                                                      SPORT[8] = 'O'
                                                else:
                                                      SPORT[8] = chr(ord(str(c % 16)) + 16)
                                          SPORT[7] = '2'
                                          for i in range(0, 10):
                                                ser2.write(SPORT[i])
                                          print '%s' % SPORT
                                          pan = ''
                                    if 'T' in pan:  # in
                                          if pan[1] == 'b' or pan[1] == 'c' or pan[1] == 'd':
                                                stop = pan[1]
                                          if pan[1] == '':
                                                pan[1] = 'b'
                                                # print "stop = %s pan[1] =%s" %  (stop,pan[1])
                                          SPORT[6] = 'I'
                                          # print "pan[1]=%s" % pan[1]
                                          # print "pan_list[]=%s" % pan_list[pan[1]]
                                          CAMR = pan_list.get(pan[1], '1')
                                          if CAMR == '':
                                                CAMR = '1'
                                          print "CAMR=%s" % CAMR
                                          c = string.atoi(str(CAMR), 10)
                                          if c % 16 == 0:
                                                SPORT[3] = str(c / 16)
                                                SPORT[8] = 'P'
                                          else:
                                                SPORT[3] = str((c / 16) + 1)
                                                if c % 16 == 10:
                                                      SPORT[8] = 'J'
                                                elif c % 16 == 11:
                                                      SPORT[8] = 'K'
                                                elif c % 16 == 12:
                                                      SPORT[8] = 'L'
                                                elif c % 16 == 13:
                                                      SPORT[8] = 'M'
                                                elif c % 16 == 14:
                                                      SPORT[8] = 'N'
                                                elif c % 16 == 15:
                                                      SPORT[8] = 'O'
                                                else:
                                                      SPORT[8] = chr(ord(str(c % 16)) + 16)
                                          SPORT[7] = '2'
                                          for i in range(0, 10):
                                                ser2.write(SPORT[i])
                                          print '%s' % SPORT
                                          pan = ''
                              if len(pan) == 3:
                                    if pan[2] == 'b' or pan[2] == 'c' or pan[2] == 'd':
                                          stop = pan[2]
                                    if pan[2] == '':
                                          pan[2] = 'b'
                                    print "stop=%s" % stop
                                    if 'U' in pan:  # Up  向上
                                          SPORT[6] = 'U'
                                          # print "pan[0]=%s" % pan[2]
                                          # print "pan_list[]=%s" % pan_list[pan[2]]
                                          CAMR = pan_list.get(pan[2], '1')
                                          if CAMR == '':
                                                CAMR = '1'
                                                # print "CAMR=%s" % CAMR
                                          c = string.atoi(CAMR, 10)
                                          if c % 16 == 0:
                                                SPORT[3] = str(c / 16)
                                                SPORT[8] = 'P'
                                          else:
                                                SPORT[3] = str((c / 16) + 1)
                                                if c % 16 == 10:
                                                      SPORT[8] = 'J'
                                                elif c % 16 == 11:
                                                      SPORT[8] = 'K'
                                                elif c % 16 == 12:
                                                      SPORT[8] = 'L'
                                                elif c % 16 == 13:
                                                      SPORT[8] = 'M'
                                                elif c % 16 == 14:
                                                      SPORT[8] = 'N'
                                                elif c % 16 == 15:
                                                      SPORT[8] = 'O'
                                                else:
                                                      SPORT[8] = chr(ord(str(c % 16)) + 16)
                                          if '1U' in pan:
                                                SPORT[7] = '1'
                                          elif '2U' in pan:
                                                SPORT[7] = '2'
                                          elif '3U' in pan:
                                                SPORT[7] = '2'
                                          elif '4U' in pan:
                                                SPORT[7] = '3'
                                          elif '5U' in pan:
                                                SPORT[7] = '4'
                                          for i in range(0, 10):
                                                ser2.write(SPORT[i])
                                          print '%s' % SPORT
                                    if 'D' in pan:  # Down  向下
                                          SPORT[6] = 'D'
                                          # print "pan[2]=%s" % pan[2]
                                          # print "pan_list[]=%s" % pan_list[pan[2]]
                                          CAMR = pan_list.get(pan[2], '1')
                                          if CAMR == '':
                                                CAMR = '1'
                                                # print "CAMR=%s" % CAMR
                                          c = string.atoi(CAMR, 10)
                                          if c % 16 == 0:
                                                SPORT[3] = str(c / 16)
                                                SPORT[8] = 'P'
                                          else:
                                                SPORT[3] = str((c / 16) + 1)
                                                if c % 16 == 10:
                                                      SPORT[8] = 'J'
                                                elif c % 16 == 11:
                                                      SPORT[8] = 'K'
                                                elif c % 16 == 12:
                                                      SPORT[8] = 'L'
                                                elif c % 16 == 13:
                                                      SPORT[8] = 'M'
                                                elif c % 16 == 14:
                                                      SPORT[8] = 'N'
                                                elif c % 16 == 15:
                                                      SPORT[8] = 'O'
                                                else:
                                                      SPORT[8] = chr(ord(str(c % 16)) + 16)
                                          if '1D' in pan:
                                                SPORT[7] = '1'
                                          elif '2D' in pan:
                                                SPORT[7] = '2'
                                          elif '3D' in pan:
                                                SPORT[7] = '2'
                                          elif '4D' in pan:
                                                SPORT[7] = '3'
                                          elif '5D' in pan:
                                                SPORT[7] = '4'
                                          for i in range(0, 10):
                                                ser2.write(SPORT[i])
                                          print '%s' % SPORT
                                    if 'R' in pan:  # Right    向右
                                          SPORT[6] = 'R'
                                          # print "tan = %s" % pan
                                          # print "pan[2]=%s" % pan[2]
                                          # print "pan_list[]=%s" % pan_list[pan[2]]
                                          CAMR = pan_list.get(pan[2], '1')
                                          if CAMR == '':
                                                CAMR = '1'
                                                # print "CAMR=%s" % CAMR
                                          c = string.atoi(CAMR, 10)
                                          if c % 16 == 0:
                                                SPORT[3] = str(c / 16)
                                                SPORT[8] = 'P'
                                          else:
                                                SPORT[3] = str((c / 16) + 1)
                                                if c % 16 == 10:
                                                      SPORT[8] = 'J'
                                                elif c % 16 == 11:
                                                      SPORT[8] = 'K'
                                                elif c % 16 == 12:
                                                      SPORT[8] = 'L'
                                                elif c % 16 == 13:
                                                      SPORT[8] = 'M'
                                                elif c % 16 == 14:
                                                      SPORT[8] = 'N'
                                                elif c % 16 == 15:
                                                      SPORT[8] = 'O'
                                                else:
                                                      SPORT[8] = chr(ord(str(c % 16)) + 16)
                                          if '1R' in pan:
                                                SPORT[7] = '1'
                                          elif '2R' in pan:
                                                SPORT[7] = '2'
                                          elif '3R' in pan:
                                                SPORT[7] = '2'
                                          elif '4R' in pan:
                                                SPORT[7] = '3'
                                          elif '5R' in pan:
                                                SPORT[7] = '4'
                                          for i in range(0, 10):
                                                ser2.write(SPORT[i])
                                          print '%s' % SPORT
                                    if 'L' in pan:  # Left  向左
                                          SPORT[6] = 'L'
                                          # print pan
                                          # print "pan[2]=%s" % pan[2]
                                          #  print "pan_list[]=%s" % pan_list[pan[2]]
                                          # CAMR = pan_list[pan[2]]
                                          CAMR = pan_list.get(pan[2], '1')
                                          if CAMR == '':
                                                CAMR = '1'
                                                # print "CAMR=%s" % CAMR
                                          c = string.atoi(str(CAMR), 10)
                                          if c % 16 == 0:
                                                SPORT[3] = str(c / 16)
                                                SPORT[8] = 'P'
                                          else:
                                                SPORT[3] = str((c / 16) + 1)
                                                if c % 16 == 10:
                                                      SPORT[8] = 'J'
                                                elif c % 16 == 11:
                                                      SPORT[8] = 'K'
                                                elif c % 16 == 12:
                                                      SPORT[8] = 'L'
                                                elif c % 16 == 13:
                                                      SPORT[8] = 'M'
                                                elif c % 16 == 14:
                                                      SPORT[8] = 'N'
                                                elif c % 16 == 15:
                                                      SPORT[8] = 'O'
                                                else:
                                                      SPORT[8] = chr(ord(str(c % 16)) + 16)
                                          if '1L' in pan:
                                                SPORT[7] = '1'
                                          elif '2L' in pan:
                                                SPORT[7] = '2'
                                          elif '3L' in pan:
                                                SPORT[7] = '2'
                                          elif '4L' in pan:
                                                SPORT[7] = '3'
                                          elif '5L' in pan:
                                                SPORT[7] = '4'
                                          if ser2.isOpen() == False:
                                                ser2.open()
                                          for i in range(0, 10):
                                                ser2.write(SPORT[i])
                                          print '%s' % SPORT
                                    pan = ''
            except:
                  pass  # 屏蔽所有异常，键盘操作异常频繁.无需理会任何未知异常 !







