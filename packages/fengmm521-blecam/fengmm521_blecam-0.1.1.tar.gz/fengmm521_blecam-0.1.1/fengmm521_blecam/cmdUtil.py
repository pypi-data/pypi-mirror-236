#!/usr/bin/python
# -*- coding: utf-8 -*-
#创建SocketServerTCP服务器：
import time
import random

LEFTDOWN = '21'     #左键按下
RIGHTDOWN = '23'    #右键按下
ALLUP     = '20'    #按键抬起

class _eventObj():
    def __init__(self,dtype,pdat):
        self.tp = dtype   #接收到的数据类型,1为鼠标坐标,2为键盘按下值
        self.dat = pdat

que = None


MAX_X = 25400   #鼠标最大逻辑x坐标
MAX_Y = 15875   #鼠标最大逻辑y坐标

class PointUtil(object):
    """docstring for Stat"""
    def __init__(self,pwh):
        self.w = pwh[0]      #手机宽像素
        self.h = pwh[1]      #手机高像素值
        self.LW = MAX_X      #点击器逻辑坐标宽度
        self.LH = MAX_Y      #点击器逻辑坐标高度
        self.dot = (float(self.LW)/float(self.w),float(self.LH)/float(self.h))
    def getLP(self,p):
        x = p[0]*self.dot[0]
        y = p[1]*self.dot[1]
        return (x,y)

POINTUTIL = None


    # time.sleep(0.001) #延时10ms
def initCmdUtil(q,pwh):
    global que,POINTUTIL
    que = q
    POINTUTIL = PointUtil(pwh)

def sendCmd(cmd):
    eobj = _eventObj(None,cmd)
    que.put(eobj)

def release(x,y):
    if not que:
        print('erro:not init cmd Queue')
    tmpp = POINTUTIL.getLP((x,y))
    tcmd = '[%d,%d,0]'%(tmpp[0],tmpp[1])
    sendCmd(tcmd)
    return tcmd + ':' + str(time.time())
def press(x,y):
    if not que:
        print('erro:not init cmd Queue')
    tmpp = POINTUTIL.getLP((x,y))
    tcmd = '[%d,%d,1]'%(tmpp[0],tmpp[1])
    sendCmd(tcmd)
    return tcmd + ':' + str(time.time())
def click(x,y):
    pcmd = press(x,y)
    pcmd = pcmd + ':' + str(time.time())
    time.sleep(0.06)
    rcmd = release(x,y)
    rcmd = rcmd + ':' + str(time.time())
    return '%s\n%s'%(pcmd,rcmd)

#按下点击笔并滑动到指定坐标x,y,然后抬起点击笔,l为按下移动的跑离,(x,y)按下后要移动到的坐标
def touchMoveTo(p1,p2,speed = 15000):
    if not que:
        print('erro:not init cmd Queue')
    tcmd = '{%d,%d,%d,%d,%d}'%(p1[0],p1[1],p2[0],p2[1],speed)
    sendCmd(tcmd)

#向左滑动
def touchMoveLeft():
    sx = int(MAX_X*0.05)
    ex = int(MAX_X*0.95)
    y = int(MAX_Y*0.5)
    dx = ex-sx
    num = 30
    stepx = int(dx/float(num))
    x = ex
    for i in range(num):
        time.sleep(0.01)
        tcmd = '[%d,%d,1]'%(x,y)
        sendCmd(tcmd)
        x -= stepx
    release(0,0)

#向右滑动
def touchMoveRight():
    sx = int(MAX_X*0.05)
    ex = int(MAX_X*0.95)
    y = int(MAX_Y*0.5)
    dx = ex-sx
    num = 30
    stepx = int(dx/float(num))
    x = sx
    for i in range(num):
        time.sleep(0.01)
        tcmd = '[%d,%d,1]'%(x,y)
        sendCmd(tcmd)
        x += stepx
    release(0,0)
#向上滑动
def touchMoveUP():
    spxmin = int(MAX_X*0.4)
    spxmax = int(MAX_X*0.6)
    
    epymin = int(MAX_Y*0.15)
    epymax = int(MAX_Y*0.2)
    
    spymin = int(MAX_Y*0.8)
    spymax = int(MAX_Y*0.85)

    randsx = random.randint(spxmin,spxmax)
    randsy = random.randint(spymin,spymax)

    randex = random.randint(spxmin,spxmax)
    randey = random.randint(epymin,epymax)
    # tcmd = '[%d,%d,1]'%(randsx,randsy)
    # sendCmd(tcmd)
    # time.sleep(0.2)
    touchMoveTo((randsx,randsy),(randex,randey),20000)

#向下滑动
def touchMoveDown():
    spxmin = int(MAX_X*0.4)
    spxmax = int(MAX_X*0.6)
    
    epymin = int(MAX_Y*0.15)
    epymax = int(MAX_Y*0.2)
    
    spymin = int(MAX_Y*0.8)
    spymax = int(MAX_Y*0.85)

    randsx = random.randint(spxmin,spxmax)
    randsy = random.randint(spymin,spymax)

    randex = random.randint(spxmin,spxmax)
    randey = random.randint(epymin,epymax)
    tcmd = '[%d,%d,1]'%(randex,randey)
    sendCmd(tcmd)
    time.sleep(0.2)
    touchMoveTo((randex,randey),(randsx,randsy),25000)

def clickKey(k):
    keycmd = None
    if type(k) == str:
        keycmd = '(~%x)'%(ord(k))
    else:
        keycmd = '(~%x)'%(k)
    sendCmd(keycmd)
#回退按键
def back():#GUI + 回退
    guikey = '(+83)'
    sendCmd(guikey)
    keycmd = '(~B2)'
    sendCmd(keycmd)
    guikey_ = '(-83)'
    sendCmd(guikey_)

def home():#GUI + 回车
    guikey = '(+83)'
    sendCmd(guikey)
    keycmd = '(~B0)'
    sendCmd(keycmd)
    guikey_ = '(-83)'
    sendCmd(guikey_)

def applist():
    #Ctrol + ESC
    guikey = '(+80)'
    sendCmd(guikey)
    keycmd = '(~B1)'
    sendCmd(keycmd)
    guikey_ = '(-80)'
    sendCmd(guikey_)

def lastApp():
    #Alt+Tab
    guikey = '(+82)'
    sendCmd(guikey)
    keycmd = '(~B3)'
    sendCmd(keycmd)
    time.sleep(3)
    keycmd = '(~B3)'
    sendCmd(keycmd)
    time.sleep(3)
    guikey_ = '(-82)'
    sendCmd(guikey_)

#
def keyboard():#GUI + /
    guikey = '(+83)'
    sendCmd(guikey)
    clickKey('/')
    guikey_ = '(-83)'
    sendCmd(guikey_)

def inputType(): #GUI + 空格  中英输入法切换
    guikey = '(+83)'
    sendCmd(guikey)
    clickKey(' ')
    guikey_ = '(-83)'
    sendCmd(guikey_)


#按下点击笔并滑动到指定坐标x,y,然后抬起点击笔,l为按下移动的跑离,(x,y)按下后要移动到的坐标
def touchMoveTo(p1,p2,speed = 10000):
    if not que:
        print('erro:not init cmd Queue')
    tcmd = '{%d,%d,%d,%d,%d}'%(p1[0],p1[1],p2[0],p2[1],speed)
    sendCmd(tcmd)
    return tcmd + ':' + str(time.time())

#主函数,程序从这里开始运行
def main():
    pass
    
if __name__ == '__main__':
    main()
    # args = sys.argv
    # fpth = ''
    # if len(args) == 2 :
    #     print('使用自定义设像头编号:')
    #     main(args[1])
    # else:
    #     print('windows系统下使用自动查找webcam摄像头')
    #     main()
    # test()


