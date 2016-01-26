#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import time
import string
import dbm
import shelve

ser = serial.Serial('/dev/ttyUSB0', 19200, 7, 'E', 1, timeout = 1)  # 配置串口
ser2 = serial.Serial('/dev/ttyUSB2', 19200, 8, 'E', 1, timeout = 1)
if ser2.isOpen() == False:
      ser2.open()
ser2.flush()
ser.flush()
UP = [0xFF, 0x01, 0x00, 0x08, 0x00, 0x3F, 0x48]
DOWN = [0xFF, 0x01, 0x00, 0x10, 0x00, 0x3F, 0x50]
LEFT = [0xFF, 0x01, 0x00, 0x04, 0x3F, 0x00, 0x44]
RIGHT = [0xFF, 0x01, 0x00, 0x02, 0x3F, 0x00, 0x42]
FAR = [0xFF, 0x01, 0x00, 0x80, 0x00, 0x00, 0x81]
HERE = [0xFF, 0x01, 0x00, 0x40, 0x00, 0x00, 0x41]
STOP = [0xFF, 0x01, 0x00, 0x20, 0x00, 0x00, 0x21]
SPORT = ['*', '2', 'A', '1', chr(0x2C), 'W', 'L', '5', 'A', chr(0x0D)]  # 通用串口云台控制
SET = ['*', '2', 'A', '1', ',', 'W', 's', '1', 'A', ',', 'W', '1', chr(0x20), 'A', chr(0x0D)]  # 设置预值位初始值
VIEW = ['*', '2', 'A', '1', ',', 'W', 'v', '1', 'A', ',', 'W', '1', chr(0x20), 'A', chr(0x0D)]  # 调用预值位初始值
rssend = ['*', '801D0,MON', chr(0x20), '1', ',CAM', chr(0x20), '1', chr(0x0D)]
cam = []
data = ''
flag = 0
count = 0
count2 = 0
flag2 = 0
MON_count = ''
CAM_count = ''
CAMt = '1'
MONt = '1'
tan = ['*2V', '1', ',', '1', chr(0x0D)]
tan2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
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

if __name__ == '__main__':
      while True:
            try:
                  # head = ser.read(12)                                              #满中断接受键盘数据
                  # print data
                  head = ser.read(1)  # 流式接受处理
                  if count2 != 0:
                        data = data + head
                  if head == '*':
                        data = data + head
                        count2 = count2 + 1
                  if head == chr(0x0D):
                        count2 = 0
                        data = data + head
                        flag2 = 1
                  if flag2 == 1:
                        flag2 = 0
                        print data
                        # print data[7]
                        # if data != '' and len(data) ==12:
                        try:
                              rev = data[7:11]
                              pan = data[7] + data[8]  # 判断云台控制状态
                              pan_stop = data[7] + data[8] + data[9] + data[10]  # 判断云台停止状态
                              speed = data[10]
                        except:
                              pass
                        data = ''
                        if count != 0:
                              count = count + 1
                              cam.append(rev[0:2])
                        if rev == '61,0' or rev == '73,0' or rev == '26,0' or rev == '74,0':  # 视频切换开始
                              count = count + 1
                              cam.append(rev[0:2])
                        if rev == '76,1':  # 视频切换截止
                              count = 0
                              flag = 1
                        if flag == 1:  # 解析出切换（输入输出）通道
                              # print cam
                              if '61' in cam:
                                    MON = cam[1::2]
                                    if '76' in MON:
                                          MON.remove('76')
                                    print MON
                                    for i in range(len(MON)):
                                          if MON[i] == '62':
                                                MON[i] = '1'
                                          if MON[i] == '63':
                                                MON[i] = '2'
                                          if MON[i] == '64':
                                                MON[i] = '3'
                                          if MON[i] == '66':
                                                MON[i] = '4'
                                          if MON[i] == '67':
                                                MON[i] = '5'
                                          if MON[i] == '68':
                                                MON[i] = '6'
                                          if MON[i] == '70':
                                                MON[i] = '7'
                                          if MON[i] == '71':
                                                MON[i] = '8'
                                          if MON[i] == '72':
                                                MON[i] = '9'
                                          if MON[i] == '75':
                                                MON[i] = '0'
                                          if MON[i] == '73':
                                                MON[i] = ''
                                          MON_count = MON_count + MON[i]
                                    print 'MON=%s' % MON_count
                                    MONt = MON_count
                                    # c = string.atoi(MONt,10)
                                    if len(MONt) > 3:
                                          MONt = '1'
                                    print MONt
                                    yy = '*2V'
                                    yy = yy + MONt + ',' + CAMt + chr(0x0D)
                                    print yy
                                    # ser2.write(yy)
                                    rssend[3] = MONt
                                    rssend[6] = CAMt
                                    for i in range(0, 8):
                                          ser.write(rssend[i])
                                    print rssend
                              if '73' in cam and '76' in cam:
                                    print cam
                                    CAM = cam[1::2]
                                    if '76' in CAM:
                                          CAM.remove('76')
                                    print CAM
                                    for i in range(len(CAM)):
                                          if CAM[i] == '62':
                                                CAM[i] = '1'
                                          if CAM[i] == '63':
                                                CAM[i] = '2'
                                          if CAM[i] == '64':
                                                CAM[i] = '3'
                                          if CAM[i] == '66':
                                                CAM[i] = '4'
                                          if CAM[i] == '67':
                                                CAM[i] = '5'
                                          if CAM[i] == '68':
                                                CAM[i] = '6'
                                          if CAM[i] == '70':
                                                CAM[i] = '7'
                                          if CAM[i] == '71':
                                                CAM[i] = '8'
                                          if CAM[i] == '72':
                                                CAM[i] = '9'
                                          if CAM[i] == '75':
                                                CAM[i] = '0'
                                          if CAM[i] == '73':
                                                CAM[i] = ''
                                          CAM_count = CAM_count + CAM[i]
                                    CAMt = CAM_count
                                    # c= string.atoi(CAMt,10)
                                    if len(CAMt) > 3:
                                          CAMt = '1'
                                    print 'CAM=%s' % CAM_count
                                    yy = '*2V'
                                    yy = yy + MONt + ',' + CAMt + chr(0x0D)
                                    print yy
                                    db = shelve.open('tantt', 'c')
                                    db[MONt] = CAMt
                                    print "db[%s] = %s" % (MONt, CAMt)
                                    db.close()
                                    ser2.write(yy)
                                    rssend[3] = MONt
                                    rssend[6] = CAMt
                                    for i in range(0, 8):
                                          ser.write(rssend[i])
                                    print rssend
                              if '26' in cam:  #set预值位
                                    CAM = cam[1::2]
                                    if '76' in CAM:
                                          CAM.remove('76')
                                    print CAM
                                    for i in range(len(CAM)):
                                          if CAM[i] == '62':
                                                CAM[i] = '1'
                                          if CAM[i] == '63':
                                                CAM[i] = '2'
                                          if CAM[i] == '64':
                                                CAM[i] = '3'
                                          if CAM[i] == '66':
                                                CAM[i] = '4'
                                          if CAM[i] == '67':
                                                CAM[i] = '5'
                                          if CAM[i] == '68':
                                                CAM[i] = '6'
                                          if CAM[i] == '70':
                                                CAM[i] = '7'
                                          if CAM[i] == '71':
                                                CAM[i] = '8'
                                          if CAM[i] == '72':
                                                CAM[i] = '9'
                                          if CAM[i] == '75':
                                                CAM[i] = '0'
                                          if CAM[i] == '73':
                                                CAM[i] = ''
                                          CAM_count = CAM_count + CAM[i]
                                    set_nu = CAM_count
                                    if len(set_nu) > 3:
                                          set_nu = '1'
                                    set_w = string.atoi(set_nu, 10)
                                    c = string.atoi(CAMt, 10)
                                    if c % 16 == 0:
                                          SET[3] = str(c / 16)
                                          SET[8] = 'P'
                                          SET[13] = 'p'
                                    else:
                                          SET[3] = str((c / 16) + 1)
                                          if c % 16 == 10:
                                                SET[8] = 'J'
                                                SET[13] = 'J'
                                          elif c % 16 == 11:
                                                SET[8] = 'K'
                                                SET[13] = 'K'
                                          elif c % 16 == 12:
                                                SET[8] = 'L'
                                                SET[13] = 'L'
                                          elif c % 16 == 13:
                                                SET[8] = 'M'
                                                SET[13] = 'M'
                                          elif c % 16 == 14:
                                                SET[8] = 'N'
                                                SET[13] = 'N'
                                          elif c % 16 == 15:
                                                SET[8] = 'O'
                                                SET[13] = 'O'
                                          else:
                                                SET[8] = chr(ord(str(c % 16)) + 16)
                                                SET[13] = chr(ord(str(c % 16)) + 16)

                                    c2 = set_w
                                    if c2 >= 16 and c2 <= 255:
                                          c3 = hex(c2)
                                          c4 = str(c3)
                                          SET[7] = c4[2]
                                          SET[11] = c4[3]
                                    elif c2 >= 1 and c2 <= 15:
                                          c3 = hex(c2)
                                          c4 = str(c3)
                                          SET[7] = '0'
                                          SET[11] = c4[2]
                                    else:
                                          print 'error!!!!'
                                    for i in range(0, 15):
                                          ser2.write(SET[i])
                                    print '%s' % SET
                              if '74' in cam:  #view调用预值位
                                    CAM = cam[1::2]
                                    if '76' in CAM:
                                          CAM.remove('76')
                                    print CAM
                                    for i in range(len(CAM)):
                                          if CAM[i] == '62':
                                                CAM[i] = '1'
                                          if CAM[i] == '63':
                                                CAM[i] = '2'
                                          if CAM[i] == '64':
                                                CAM[i] = '3'
                                          if CAM[i] == '66':
                                                CAM[i] = '4'
                                          if CAM[i] == '67':
                                                CAM[i] = '5'
                                          if CAM[i] == '68':
                                                CAM[i] = '6'
                                          if CAM[i] == '70':
                                                CAM[i] = '7'
                                          if CAM[i] == '71':
                                                CAM[i] = '8'
                                          if CAM[i] == '72':
                                                CAM[i] = '9'
                                          if CAM[i] == '75':
                                                CAM[i] = '0'
                                          if CAM[i] == '73':
                                                CAM[i] = ''
                                          CAM_count = CAM_count + CAM[i]
                                    view_nu = CAM_count
                                    if len(view_nu) > 3:
                                          view_nu = '1'
                                    view_w = string.atoi(view_nu, 10)

                                    c = string.atoi(CAMt, 10)
                                    if c % 16 == 0:
                                          VIEW[3] = str(c / 16)
                                          VIEW[8] = 'P'
                                          VIEW[13] = 'p'
                                    else:
                                          VIEW[3] = str((c / 16) + 1)
                                          if c % 16 == 10:
                                                VIEW[8] = 'J'
                                                VIEW[13] = 'J'
                                          elif c % 16 == 11:
                                                VIEW[8] = 'K'
                                                VIEW[13] = 'K'
                                          elif c % 16 == 12:
                                                VIEW[8] = 'L'
                                                VIEW[13] = 'L'
                                          elif c % 16 == 13:
                                                VIEW[8] = 'M'
                                                VIEW[13] = 'M'
                                          elif c % 16 == 14:
                                                VIEW[8] = 'N'
                                                VIEW[13] = 'N'
                                          elif c % 16 == 15:
                                                VIEW[8] = 'O'
                                                VIEW[13] = 'O'
                                          else:
                                                VIEW[8] = chr(ord(str(c % 16)) + 16)
                                                VIEW[13] = chr(ord(str(c % 16)) + 16)

                                    c2 = view_w
                                    if c2 >= 16 and c2 <= 255:
                                          c3 = hex(c2)
                                          c4 = str(c3)
                                          VIEW[7] = c4[2]
                                          VIEW[11] = c4[3]
                                    elif c2 >= 1 and c2 <= 15:
                                          c3 = hex(c2)
                                          c4 = str(c3)
                                          VIEW[7] = '0'
                                          VIEW[11] = c4[2]
                                    else:
                                          print 'error!!!!'
                                    for i in range(0, 15):
                                          ser2.write(VIEW[i])
                                    print '%s' % VIEW

                                    # if string.atoi(MON_count,10) <=32 and string.atoi(CAM_count,10) <= 128:
                                    #   ser2.write(yy)                                                   #发送切换指令
                                    # yy = '*1V'
                              cam = []
                              CAM_count = ''
                              MON_count = ''
                              flag = 0
                        # SPORT  = ['*','1','A','4',chr(0x2C),'W','L','5','A',chr(0x0D)]
                        if pan == '99':  #right
                              SPORT[6] = 'R'
                              if pan_stop == '99,0':
                                    SPORT[6] = 'H'
                                    # print CAMt,MONt
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.05)

                        elif pan == '98':  #left
                              SPORT[6] = 'L'
                              if pan_stop == '98,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              if ser2.isOpen() == False:
                                    ser2.open()
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.04)
                        elif pan == '97':  #down
                              SPORT[6] = 'D'
                              if pan_stop == '97,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.05)
                        elif pan == '96':  #up
                              SPORT[6] = 'U'
                              if pan_stop == '96,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.05)
                        elif pan == '90':  #here
                              SPORT[6] = 'N'
                              if pan_stop == '90,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.05)
                        elif pan == '91':  #far
                              SPORT[6] = 'F'
                              if pan_stop == '91,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.05)
                        elif pan == '86':
                              SPORT[6] = 'I'
                              if pan_stop == '86,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.05)
                        elif pan_stop == '65,0':
                              c = string.atoi(CAMt, 10)
                              c = c + 1
                              if c > 128:
                                    c = 1
                              CAMt = str(c)
                              yy = '*2V'
                              yy = yy + MONt + ',' + CAMt + chr(0x0D)
                              print yy
                              ser2.write(yy)
                              rssend[3] = MONt
                              rssend[6] = CAMt
                              for i in range(0, 8):
                                    ser.write(rssend[i])
                              print rssend

                        elif pan_stop == '69,0':
                              c = string.atoi(CAMt, 10)
                              c = c - 1
                              if c == 0:
                                    c = 1
                              CAMt = str(c)
                              yy = '*2V'
                              yy = yy + MONt + ',' + CAMt + chr(0x0D)
                              print yy
                              ser2.write(yy)
                              rssend[3] = MONt
                              rssend[6] = CAMt
                              for i in range(0, 8):
                                    ser.write(rssend[i])
                              print rssend

                        elif pan == '87':
                              SPORT[6] = 'O'
                              if pan_stop == '87,0':
                                    SPORT[6] = 'H'
                              if CAMt == '':
                                    CAMt = '1'
                              c = string.atoi(CAMt, 10)
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
                              SPORT[7] = speed
                              for i in range(0, 10):
                                    ser2.write(SPORT[i])
                              print '%s' % SPORT
                              time.sleep(0.1)
                        if speed == '0':
                              SPORT[5] = 'H'
                              c = string.atoi(CAMt, 10)
                              SPORT[3] = str((c / 16) + 1)
                              if c % 16 == 0:
                                    SPORT[7] = 'P'
                              else:
                                    SPORT[7] = chr(ord(c % 16) - 8)
                              SPORT[6] = speed
                              for i in range(0, 8):
                                    ser2.write(SPORT[i])
            except:
                  pass  # 屏蔽所有未知异常
ser.close()
ser2.close()
#

