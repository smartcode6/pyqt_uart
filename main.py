# *coding:utf-8 *
# from serial_ui import Ui_Form
# import sys
# import PyQt5.QtWidgets as qw

# import sys
# from PyQt5.QtWidgets import QWidget, QApplication
# import serial_ui


# class InitForm(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.ui = serial_ui.Ui_Form()
#         self.ui.setupUi(self)
#         self.setWindowTitle("串口助手")
#
#     def closeEvent(self, event):
#         print("窗体关闭")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w1 = InitForm()
#     w1.show()
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtWidgets import QApplication,QWidget
# from serial_ui import Ui_Form
#
# class InitFrom(QWidget):
#     def __init__(self):
#         super(InitFrom, self).__init__()
#         self.ui=Ui_Form()
#         self.ui.setupUi(self)
#         self.setWindowTitle('串口')
#
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     w=InitFrom()
#     w.show()
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtWidgets import QApplication,QWidget
# from serial_ui import Ui_Form
# class InitFrom(QWidget):
#     def __init__(self):
#         super(InitFrom, self).__init__()
#         self.ui=Ui_Form()
#         self.ui.setupUi(self)
#         self.setWindowTitle('你好')
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     w=InitFrom()
#     w.show()
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtWidgets import QApplication,QWidget
# from serial_ui import Ui_Form
# import time
# class InitFrom(QWidget):
#     def __init__(self):
#         super(InitFrom, self).__init__()
#         self.ui=Ui_Form()
#         self.ui.setupUi(self)
#         self.setWindowTitle('hello')
# if __name__ =='__main__':
#     app = QApplication(sys.argv)
#     w=InitFrom()
#     w.show()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication,QWidget
from serial_ui import Ui_Form
from serial_thread import MySerial
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import QThread
import threading
import time
class InitFrom(QWidget):
    def __init__(self):
        super(InitFrom, self).__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('串口助手')
        print('主线程ID', threading.current_thread().ident)
        self.ui_init()#初始化UI界面，包括一些下拉框的默认填充值
        self.scan_com()#扫描一次com口
        self.ui_control_cb_init() #初始化窗口控件的槽函数
        self.serial_thread_init()#初始化串口线程
        self.flag_open_close=0
    def ui_init(self):
        self.baud=('115200','9600','4800','57600','921600')
        self.data=('8','5','6','7')
        self.stop=('1','2')
        self.parity=('None','Even','Odd')

        self.ui.com_box_baud.addItems(self.baud)
        self.ui.com_box_datas.addItems(self.data)
        self.ui.com_box_stop.addItems(self.stop)
        self.ui.com_box_parity.addItems(self.parity)
    def ui_control_cb_init(self):
        self.ui.push_btn_open_close.clicked.connect(self.push_btn_open_close_cb)
        self.ui.push_btn_com_flush.clicked.connect(self.push_btn_com_flush_cb)
        self.ui.push_btn_send.clicked.connect(self.push_btn_send_cb)
        self.ui.push_btn_clear_recv.clicked.connect(self.push_btn_clear_recv_cb)
    #初始化主线程和串口线程建立连接的signal
    def serial_thread_init(self):
        self.my_serial_handle=MySerial()
        self.serial_thread=QThread()
        self.my_serial_handle.moveToThread(self.serial_thread)
        self.serial_thread.start()
        self.my_serial_handle.sig_serial_init.connect(self.my_serial_handle.serial_init)
        self.my_serial_handle.sig_serial_init.emit()
        self.my_serial_handle.sig_com_open_close.connect(self.my_serial_handle.slot_serial_com_open_close)
        self.my_serial_handle.sig_send_data.connect(self.my_serial_handle.slot_serial_write)
        self.my_serial_handle.sig_recv_data.connect(self.slot_recv_data)
    def scan_com(self):
        print('串口刷新')
        availab_com=QSerialPortInfo.availablePorts()
        all_com=[]
        for com in availab_com:
            all_com.append(com.portName())
        self.ui.com_box_com.addItems(all_com)
    def push_btn_open_close_cb(self):
        print('点击了串口打开关闭按钮')
        com_para={}
        com_para['com']=self.ui.com_box_com.currentText()
        com_para['baud']=self.ui.com_box_baud.currentText()
        com_para['data']=self.ui.com_box_datas.currentText()
        com_para['stop']=self.ui.com_box_stop.currentText()
        com_para['parity']=self.ui.com_box_parity.currentText()
        if self.flag_open_close==0:
            print('之前串口关闭，现在打开')
            com_para['flag']=1
            self.flag_open_close=1
            self.ui.push_btn_open_close.setText('关闭串口')
            self.ui.push_btn_open_close.setStyleSheet('color:red')
        else:
            print('之前串口打开，现在关闭')
            self.flag_open_close=0
            com_para['flag'] = 0
            self.ui.push_btn_open_close.setText('打开串口')
            self.ui.push_btn_open_close.setStyleSheet('color:black')
        self.my_serial_handle.sig_com_open_close.emit(com_para)
        time.sleep(0.01)

        pass
    def push_btn_com_flush_cb(self):
        self.scan_com()
        print('点击了串口刷新按钮')
        pass
    def push_btn_send_cb(self):
        print('点击了发送按钮')
        send_data={}
        send_data['data']=self.ui.text_edit_send.toPlainText()
        self.my_serial_handle.sig_send_data.emit(send_data)
        print('主线程发送的数据', send_data, threading.current_thread().ident)
        pass
    def push_btn_clear_recv_cb(self):
        pass
    def slot_recv_data(self,data):
        print('ui线程收到了数据',data)
        show_buff=bytes(data)
        print(show_buff)
        self.ui.text_edit_recv.insertPlainText(show_buff.decode('utf-8','ignore'))
        pass
if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=InitFrom()
    w.show()
    sys.exit(app.exec_())
