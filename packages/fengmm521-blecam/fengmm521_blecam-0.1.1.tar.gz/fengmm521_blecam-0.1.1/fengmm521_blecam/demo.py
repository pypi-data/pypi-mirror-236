
import imp
import os,sys
from fengmm521_blecam import cmdUtil

from fengmm521_blecam import cvUtil
from fengmm521_blecam import serialUtil
from fengmm521_blecam import httpUtil

from queue import Queue
import time


# IMGSIZE = (720,1650) 
IMGSIZE = (1080,2160) #红米

CMDQUEUE = Queue()

MousePress = False

logPth = str(int(time.time())) + '.txt'

lastTime = time.time()*1000

imgNum = 1
imgMax = -1

os.getcwd()

imgPth = './img' + os.sep + '%d.jpg'%(imgNum)
def setImgNum(n):
    global imgPth,imgNum,imgMax
    tmpimg = '%d.jpg'%(n)
    if os.path.exists('./img' + os.sep + tmpimg):
        imgPth = tmpimg
        imgNum = n
    else:
        print('img pth empty:%s'%(tmpimg))
        if n > imgNum:
            imgMax = imgNum
            imgNum = 1
            imgPth = '%d.jpg'%(imgNum)
        else:
            if imgMax == -1:
                imgNum = 1
                imgPth = '%d.jpg'%(imgNum) 
            else:
                imgNum = imgMax
                imgPth = '%d.jpg'%(imgNum) 
    imgPth = './img' + os.sep + imgPth
def onMove(x,y,flogs):
    if MousePress:
        onPress(x,y,flogs)
    else:
        onRelease(x,y,flogs)

def saveCmdToFile(cmd):
    f = open(logPth,'a+')
    f.write(cmd + '\n')
    f.close()

moveP = None

def onPress(x,y,flogs):
    global MousePress,moveP
    MousePress = True
    print('press',(x,y),'flogs',flogs)
    if flogs >= 8 and flogs <= 15:    #ctrl 按键按下的点击,保存按下指令
        cmd = cmdUtil.press(x,y)
        saveCmdToFile(cmd)
    elif flogs >= 32 and flogs <= 39: #alt 按键按下事件,为使用两点移动指令,并保存指令
        if not moveP:
            moveP = (x,y)
        else:
            cmd = cmdUtil.touchMoveTo(moveP,(x,y))
            saveCmdToFile(cmd)
    elif flogs >= 16 and flogs <= 31: #shift 按键按下事件,两点移动指令,不保存指令
        if not moveP:
            moveP = (x,y)
        else:
            cmd = cmdUtil.touchMoveTo(moveP,(x,y))
    else:
        #按下指令,不保存指令
        cmd = cmdUtil.press(x,y)
def onRelease(x,y,flogs):
    global MousePress
    MousePress = False
    print('release',(x,y),'flogs',flogs)
    cmd = cmdUtil.release(x,y)
    if flogs >= 8 and flogs <= 15:    #ctrl 按键抬起的点击,保存按下指令
        saveCmdToFile(cmd)

def onImgSizeChange(s):
    global IMGSIZE
    IMGSIZE = s
    print(s)
    cmdUtil.initCmdUtil(CMDQUEUE,IMGSIZE)
    
def onKeyDown(cvobj,key):
    global logPth
    if key & 0xFF == 0x1B:
        exit(0)                                 
    if key & 0xFF == 0x20: #空格按下,使用adb工具截取手机屏画面显示内容
        print('space down')
        # cvobj.showAdbImg()
    else:
        print('on key down:%x'%(key))
        pt = (0,0)
        if key & 0xFF == ord('h'):##归零操作
            print('on key down:%s'%(chr(key)))
            cmdUtil.release(0,0)
            return
        elif (key & 0xFF == 0x0D):##回车,开启一个新脚本
            logPth = str(int(time.time())) + '.txt'
            print('open one New file name:%s'%(logPth))
        elif (key & 0xFF == ord('q')):#app列表
            print('q key down')
            cmdUtil.applist()
        elif (key & 0xFF == ord('w')):#返回主界面
            print('w key down')
            cmdUtil.home()
        elif (key & 0xFF == ord('e')):#回退
            print('e key down')
            cmdUtil.back()
        elif (key & 0xFF == ord('a')):##显示键盘快捷键
            print('a key down')
            cmdUtil.keyboard()
        elif (key & 0xFF == ord('s')):##输入法切换
            print('s key down')
            cmdUtil.inputType()
        elif (key & 0xFF == ord('d')):##上一个app
            print('i key down')
            cmdUtil.lastApp()
        elif (key & 0xFF == ord('z')):#向左滑动
            print('p key down')
            cmdUtil.touchMoveLeft()
        elif (key & 0xFF == ord('x')):#向右滑动
            print('p key down')
            cmdUtil.touchMoveRight()
        elif key & 0xFF == ord(',') or key & 0xFF == ord('<'): #向上滑动
            print(', key down')
            cmdUtil.touchMoveUP()
        elif key & 0xFF == ord('.') or key & 0xFF == ord('>'): #向下滑动
            print('. key down')
            cmdUtil.touchMoveDown()
        elif key & 0xFF == ord('t'):#运行测试脚本
            print('t key down')
        elif key == 9:#tab键
            print('tab key down')
        elif key & 0xFF == ord('v'):#保存图片
            cvobj.saveLastImg()
        elif key & 0xFF == ord('r'):#运行run脚本中的run函数
            #运行脚本
            print('r key down')
        elif key & 0xFF == ord('o'):#o键,使用ocr识别图片中的文字
            # print('http ocr')
            print('o key down')
            httpUtil.httpPostImg(cvobj.baseImg,ip = '192.168.1.8',port=8889)
            # testScrpit(cvobj,PSobj,DPobj,ImgPobj,SOCKETQUEUE,'ocr')
        elif key & 0xFF == ord('y'):#y键,使用yolo识别图片中训练的图片
            # print('http yolo')
            print('y key down')
            # testScrpit(cvobj,PSobj,DPobj,ImgPobj,SOCKETQUEUE,'yolo')
        elif key & 0xFF >= ord('n'):#停止正在运行的脚本
            # stopScrpit()
            print('n key down')
        elif key & 0xFF == ord('1'):#F1键,调整焦距,每次+100个单位
            print('F1键,调整焦距,每次+100个单位')
            cvobj.camobj.addFocus(100)
            time.sleep(0.1)
        elif key & 0xFF == ord('2'):#F2键,调整焦距,每次-100个单位
            print('F2键,调整焦距,每次-100个单位')
            cvobj.camobj.subFocus(100)
            time.sleep(0.1)
        elif key & 0xFF == ord('3'):##F3键,调整焦距,每次+10个单位
            print('F3键,调整焦距,每次+10个单位')
            cvobj.camobj.addFocus(10)
            time.sleep(0.1)
        elif key & 0xFF == ord('4'):#F4键,调整焦距,每次-10个单位
            print('F4键,调整焦距,每次-10个单位')
            cvobj.camobj.subFocus(10)
        elif key & 0xFF == ord('5'):#F5键,调整焦距,每次+1个单位
            print('F5键,调整焦距,每次+1个单位')
            cvobj.camobj.addFocus(1)
        elif key & 0xFF == ord('6'):#F6键,调整焦距,每次-1个单位
            print('F6键,调整焦距,每次-1个单位')
            cvobj.camobj.subFocus(1)
        elif key & 0xFF == ord('7'):#设置爆光度减小
            print('7键,调整爆光度,减1')
            cvobj.camobj.subExposure()
        elif key & 0xFF == ord('8'):#设置爆光度增大
            print('8键,调整爆光度,加1')
            cvobj.camobj.addExposure()
        elif key & 0xFF == 118:#F7键
            print('F3 key down')
        elif key & 0xFF == 119:#F8键
            print('F4 key down')
            
def main(camID = 0):
    net_thread = serialUtil.serialThread(CMDQUEUE)
    net_thread.setDaemon(True)
    net_thread.start()
    time.sleep(3)
    cmdUtil.initCmdUtil(CMDQUEUE,IMGSIZE)
    cvimgobj = cvUtil.cv2Stream(CMDQUEUE,imgPth,onPress,onRelease,onMove,onKeyDown,onImgSizeChange,IMGSIZE,camID)
    cvimgobj.start()

if __name__ == '__main__':  
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        print('如果找不到webcam摄像头,将使用自定义设像头编号:%d',args[1])
        main(int(args[1]))
    else:
        print('windows系统下使用自动查找webcam摄像头')
        main()
