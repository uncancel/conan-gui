#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import sys, os, urllib, zipfile, ConfigParser, win32con, win32api, win32gui, threading


class Conan_ui(QtGui.QMainWindow):
    def __init__(self):
        super(Conan_ui, self).__init__()
        self.area_1()
        self.area_2()
        self.area_3()
        self.area_4()
        
        self.main_window()
        
    def area_1(self):    
        self.lbl1 = QtGui.QLabel(u'服务端安装路径：', self)
        self.lbl1.move(10, 10)
        
        self.ledt1 = QtGui.QLineEdit(self)    #显示服务端安装路径
        self.ledt1.setGeometry(105, 10, 400, 30)
        self.ledt1.setReadOnly(True)
        
        self.btn1 = QtGui.QPushButton(u'浏览', self)    #浏览按钮
        self.btn1.setGeometry(520, 10, 50, 30)
        self.btn1.clicked.connect(self.select_dir)    #点击按钮选择安装路径
        
        self.btn_ex1 = QtGui.QPushButton(u'读取服务端设置', self)
        self.btn_ex1.setGeometry(585, 10, 100, 30)
        self.btn_ex1.clicked.connect(self.set_default)
        
        self.btn2 = QtGui.QPushButton(u'安装/更新', self)    #安装按钮
        self.btn2.setGeometry(700, 10, 80, 30)
        self.btn2.clicked.connect(self.multi_proc_download)    #点击按钮安装steamcmd和服务端 
    
    def area_2(self):
        self.btn3 = QtGui.QPushButton('start', self)
        self.btn3.setGeometry(10, 55, 110, 40)
        self.btn3.setIcon(QtGui.QIcon('image\start.png'))
        self.btn3.clicked.connect(self.multi_proc_start)
        
        self.btn4 = QtGui.QPushButton('stop', self)
        self.btn4.setGeometry(130, 55, 110, 40)
        self.btn4.setIcon(QtGui.QIcon('image\stop.png'))
        self.btn4.clicked.connect(self.ctrl_c)
        
        self.btn5 = QtGui.QPushButton(u'应用设置', self)
        self.btn5.setGeometry(300, 55, 150, 40)
        self.btn5.clicked.connect(self.modifiy_ini_)
    
    def area_3(self):
        area_3_y = 100    #area_3 基础Y坐标
        
        self.lbl2 = QtGui.QLabel(u'服务器设置', self)
        self.lbl2.setFont(QtGui.QFont(u"微软雅黑", 14, QtGui.QFont.Bold)) 
        self.lbl2.setGeometry(10, area_3_y, 150, 40)
        
        self.lbl3 = QtGui.QLabel(u'服务器名称：', self)
        self.lbl3.move(10, area_3_y+45)
        self.ledt2 = QtGui.QLineEdit(self)
        self.ledt2.setGeometry(82, area_3_y+45, 200, 30)
        
        self.lbl4 = QtGui.QLabel(u'服务器密码：', self)
        self.lbl4.move(310, area_3_y+45)
        self.ledt3 = QtGui.QLineEdit(self)
        self.ledt3.setGeometry(380, area_3_y+45, 200, 30)
        
        self.lbl5 = QtGui.QLabel(u'服务器最大人数：', self)
        self.lbl5.move(600, area_3_y+45)
        self.ledt4 = QtGui.QLineEdit(self)
        self.ledt4.setGeometry(695, area_3_y+45, 40, 30)
        
        self.lbl_ex1 = QtGui.QLabel(u'服务器管理员密码：', self)
        self.lbl_ex1.move(10, area_3_y+90)
        self.ledt_ex1 = QtGui.QLineEdit(self)
        self.ledt_ex1.setGeometry(120, area_3_y+90, 200, 30)
        
        self.chkb1 = QtGui.QCheckBox(u'PVP模式', self)
        self.chkb1.move(10, area_3_y+135)
        self.connect(self.chkb1, QtCore.SIGNAL('stateChanged(int)'), self.change_chkb_value)
        
        self.chkb2 = QtGui.QCheckBox(u'死亡丢失装备', self)
        self.chkb2.move(160, area_3_y+135)
        self.connect(self.chkb2, QtCore.SIGNAL('stateChanged(int)'), self.change_chkb_value)
        
        self.chkb3 = QtGui.QCheckBox(u'2', self)
        self.chkb3.move(310, area_3_y+135)
        
        self.chkb4 = QtGui.QCheckBox(u'3', self)
        self.chkb4.move(460, area_3_y+135)
        
        self.chkb5 = QtGui.QCheckBox(u'4', self)
        self.chkb5.move(610, area_3_y+135)
    
    def area_4(self):
        area_4_x = 180
        area_4_y = 270
        
        self.lbl6 = QtGui.QLabel(u'游戏参数设置', self)
        self.lbl6.setFont(QtGui.QFont(u"微软雅黑", 14, QtGui.QFont.Bold)) 
        self.lbl6.setGeometry(10, area_4_y, 150, 40)
##############################################################################################        
        self.lbl7 = QtGui.QLabel(u'A:', self)
        self.lbl7.move(10, area_4_y+45)
        self.ledt5 = QtGui.QLineEdit(self)
        self.ledt5.setGeometry(80, area_4_y+45, 80, 30)
        
        self.lbl8 = QtGui.QLabel(u'B:', self)
        self.lbl8.move(10 + area_4_x, area_4_y+45)
        self.ledt6 = QtGui.QLineEdit(self)
        self.ledt6.setGeometry(80 + area_4_x, area_4_y+45, 80, 30)
       
        self.lbl9 = QtGui.QLabel(u'C:', self)
        self.lbl9.move(10 + area_4_x*2, area_4_y+45)
        self.ledt7 = QtGui.QLineEdit(self)
        self.ledt7.setGeometry(80 + area_4_x*2, area_4_y+45, 80, 30)
        
        self.lbl10 = QtGui.QLabel(u'D:', self)
        self.lbl10.move(10 + area_4_x*3, area_4_y+45)
        self.ledt8 = QtGui.QLineEdit(self)
        self.ledt8.setGeometry(80 + area_4_x*3, area_4_y+45, 80, 30)
##############################################################################################        
        self.lbl11 = QtGui.QLabel(u'E:', self)
        self.lbl11.move(10, area_4_y+90)
        self.ledt9 = QtGui.QLineEdit(self)
        self.ledt9.setGeometry(80, area_4_y+90, 80, 30)
        
        self.lbl12 = QtGui.QLabel(u'F:', self)
        self.lbl12.move(10 + area_4_x, area_4_y+90)
        self.ledt10 = QtGui.QLineEdit(self)
        self.ledt10.setGeometry(80 + area_4_x, area_4_y+90, 80, 30)
       
        self.lbl13 = QtGui.QLabel(u'G:', self)
        self.lbl13.move(10 + area_4_x*2, area_4_y+90)
        self.ledt11 = QtGui.QLineEdit(self)
        self.ledt11.setGeometry(80 + area_4_x*2, area_4_y+90, 80, 30)
        
        self.lbl14 = QtGui.QLabel(u'H:', self)
        self.lbl14.move(10 + area_4_x*3, area_4_y+90)
        self.ledt12 = QtGui.QLineEdit(self)
        self.ledt12.setGeometry(80 + area_4_x*3, area_4_y+90, 80, 30)
##############################################################################################
        self.lbl15 = QtGui.QLabel(u'I:', self)
        self.lbl15.move(10, area_4_y+135)
        self.ledt13 = QtGui.QLineEdit(self)
        self.ledt13.setGeometry(80, area_4_y+135, 80, 30)
        
        self.lbl16 = QtGui.QLabel(u'J:', self)
        self.lbl16.move(10 + area_4_x, area_4_y+135)
        self.ledt14 = QtGui.QLineEdit(self)
        self.ledt14.setGeometry(80 + area_4_x, area_4_y+135, 80, 30)
       
        self.lbl17 = QtGui.QLabel(u'K:', self)
        self.lbl17.move(10 + area_4_x*2, area_4_y+135)
        self.ledt15 = QtGui.QLineEdit(self)
        self.ledt15.setGeometry(80 + area_4_x*2, area_4_y+135, 80, 30)
        
        self.lbl18 = QtGui.QLabel(u'L:', self)
        self.lbl18.move(10 + area_4_x*3, area_4_y+135)
        self.ledt16 = QtGui.QLineEdit(self)
        self.ledt16.setGeometry(80 + area_4_x*3, area_4_y+135, 80, 30)
            
    def main_window(self):
        self.setGeometry(300, 300, 800, 600)    #主窗口
        self.setWindowTitle(u"流放者柯南服务端管理器   Ver 1.0")
        self.setWindowIcon(QtGui.QIcon('image\icon.jpg'))
        self.center()
        self.statusBar()
        self.update()    #update()触发paintEvent()画线
        self.show()
        
        if self.get_ini('setting.ini', 'serverpath', 'serverpath'):    #从setting.ini中读取上次保存的服务端路径
            self.ledt1.setText(self.get_ini('setting.ini', 'serverpath', 'serverpath'))
            self.dir_path = self.get_ini('setting.ini', 'serverpath', 'serverpath')    
        else:
            self.dir_path = 'd:\\'
        self.chkb1_value = 'False'  #单选框的默认值
        self.chkb2_value = 'False'
        
    def install_steamcmd(self):    #安装steamcmd并且安装柯南服务端
        zip_path = os.path.join(self.dir_path, 'steamcmd.zip') #保存路径
        if os.path.exists(self.dir_path):
            self.statusBar().showMessage('update conan server...')
            os.system('%s\steamcmd\steamcmd.exe +force_install_dir %s +login anonymous +app_update 443030 validate' % (self.dir_path, self.dir_path)) #运行steamcmd.exe,并下载服务端
        else:
            os.mkdir(self.dir_path)
        
            if os.path.exists(zip_path):
                self.error_jump('steamcmd.zip already exist!')
            else:
                self.statusBar().showMessage("downloading steamcmd...")
                urllib.urlretrieve("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", zip_path) #开始下载

            if os.path.exists(self.dir_path + '\steamcmd\steamcmd.exe'):
                self.error_jump('steamcmd.exe already exist!')
            else:
                self.statusBar().showMessage('unzipping steamcmd.zip')
                steamzip = zipfile.ZipFile(zip_path)  #读取zip文件
                steamzip.extractall(self.dir_path +'\steamcmd')  #解压路径
                steamzip.close()
                if os.path.exists(zip_path):  #删除zip文件
                    os.remove(zip_path)
                if os.path.exists(self.dir_path + '\ConanSandboxServer.exe'):
                    self.error_jump(u'路径中已有服务端文件，请确认')
                else:
                    self.statusBar().showMessage('download conan server...')
                    os.system('%s\steamcmd\steamcmd.exe +force_install_dir %s +login anonymous +app_update 443030 validate' % (self.dir_path, self.dir_path)) #运行steamcmd.exe,并下载服务端
    
    def select_dir(self):    #弹出选择路径窗口
        self.dir_path = unicode(QtGui.QFileDialog.getExistingDirectory(self, u"选择服务端安装路径", "D:\\")) + "\conanexiles"
        self.modify_ini('setting.ini', 'serverpath', 'serverpath', self.dir_path)
        if self.dir_path:
            self.ledt1.setText(self.dir_path)    #将路径显示在文本框中
    
    def paintEvent(self, e):    #画图事件,画分割线
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.blue,1))
        for i in range(0, 4000, 4):
            qp.drawPoint(i, 50 )
        for i in range(0, 4000, 4):
            qp.drawPoint(i, 100 )
        qp.end()
    
    def start_server(self):
        if os.path.exists(self.dir_path+'\ConanSandboxServer.exe'):
            os.system('%s\ConanSandboxServer.exe -log' % self.dir_path)    #运行服务端
        else:
            self.error_jump(u'未找到文件，请选择正确的路径')
            
    def change_chkb_value(self):    #检查单选框是否被勾选，并由此改变T OR F
        if self.chkb1.isChecked():
            self.chkb1_value = 'True'
        else:
            self.chkb1_value = 'False'
           
        if self.chkb2.isChecked():
            self.chkb2_value = 'True'
        else:
            self.chkb2_value = 'False'
            
    def error_jump(self, error_message):    #弹出错误提示窗口
        self.msgb1 = QtGui.QMessageBox.warning(self,
                                               "Warning",  
                                               error_message,  
                                               QtGui.QMessageBox.Cancel,  
                                               QtGui.QMessageBox.Cancel) 
    
    def multi_proc_download(self):   #多线程，解决安装时程序未响应
        sub_proc = threading.Thread(target = self.install_steamcmd)
        sub_proc.daemon = True
        sub_proc.start()        
    
    def multi_proc_start(self):   #多线程，解决运行服务端时程序未响应
        sub_proc = threading.Thread(target = self.start_server)
        sub_proc.daemon = True
        sub_proc.start()
    
    def ctrl_c(self):    #寻找窗口，并发送ctrl+c关闭窗口
        win = win32gui.FindWindow(None,  self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultEngine.ini', 'OnlineSubsystem', 'ServerName') + ' - Conan Exiles - press Ctrl+C to shutdown')
        
        if win:
            win32gui.ShowWindow(win,1)   
            win32gui.SetForegroundWindow (win)
            
            win32api.keybd_event(17,0,0,0)  
            win32api.keybd_event(67,0,0,0)  
            win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0) 
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
        else:
            pass
    
    def modify_ini(self, file_name, section_name, attribute_name, update_value): #修改ini内容
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(file_name)
        if update_value == '':    #如果没有输入，则不做改变
            pass
        else:
            config.set(section_name, attribute_name, update_value)
        config.write(open(file_name, 'w+'))

    def modifiy_ini_(self):
        self.modify_ini(self.dir_path + '\ConanSandbox\Config\DefaultEngine.ini', 'OnlineSubsystem', 'ServerName', self.ledt2.text())
        self.modify_ini(self.dir_path + '\ConanSandbox\Config\DefaultEngine.ini', 'OnlineSubsystem', 'ServerPassword', self.ledt3.text())
        self.modify_ini(self.dir_path + '\ConanSandbox\Config\DefaultGame.ini', '/Script/Engine.GameSession', 'MaxPlayers', self.ledt4.text())
        self.modify_ini(self.dir_path + '\ConanSandbox\Config\DefaultServerSettings.ini', 'ServerSettings', 'AdminPassword', self.ledt_ex1.text())
        self.modify_ini(self.dir_path + '\ConanSandbox\Config\DefaultServerSettings.ini', 'ServerSettings', 'PVPEnabled', self.chkb1_value)
        self.modify_ini(self.dir_path + '\ConanSandbox\Config\DefaultServerSettings.ini', 'ServerSettings', 'DropEquipmentOnDeath', self.chkb2_value)
    
    def get_ini(self, file_name, section_name, attribute_name):    #读取ini文件中的配置
        config = ConfigParser.ConfigParser()
        config.read(file_name)
        return config.get(section_name, attribute_name)
        
    def set_default(self):    #读取修改前的设置并显示在文本框中
        if os.path.exists(self.dir_path + '\ConanSandbox\Saved\Config\WindowsServer\ServerSettings.ini'):
            self.ledt2.setText(self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultEngine.ini', 'OnlineSubsystem', 'ServerName'))
            self.ledt3.setText(self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultEngine.ini', 'OnlineSubsystem', 'ServerPassword'))
            self.ledt4.setText(self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultGame.ini', '/Script/Engine.GameSession', 'MaxPlayers'))
            self.ledt_ex1.setText(self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultServerSettings.ini', 'ServerSettings', 'AdminPassword'))
            
            if self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultServerSettings.ini', 'ServerSettings', 'PVPEnabled') == 'True':    #检查单选框初始状态        
                self.chkb1.setChecked (True)
            else:
                self.chkb1.setChecked (False)
            if self.get_ini(self.dir_path + '\ConanSandbox\Config\DefaultServerSettings.ini', 'ServerSettings', 'DropEquipmentOnDeath') == 'True':    #检查单选框初始状态        
                self.chkb2.setChecked (True)
            else:
                self.chkb2.setChecked (False)
        else:
            self.error_jump(u'未检测到配置文件，请先运行一次服务端或检查路径是否错误')
#            self.ledt2.setReadOnly(True)
#            self.ledt3.setReadOnly(True)
#            self.ledt4.setReadOnly(True)
#            self.ledt5.setReadOnly(True)
#            self.ledt6.setReadOnly(True)
#            self.ledt7.setReadOnly(True)
#            self.ledt8.setReadOnly(True)
#            self.ledt9.setReadOnly(True)
#            self.ledt10.setReadOnly(True)
#            self.ledt11.setReadOnly(True)
#            self.ledt12.setReadOnly(True)
#            self.ledt13.setReadOnly(True)
#            self.ledt14.setReadOnly(True)
#            self.ledt15.setReadOnly(True)
#            self.ledt16.setReadOnly(True)
    
    def center(self):    #让窗口显示在屏幕中央
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    ex = Conan_ui()
    sys.exit(app.exec_())
