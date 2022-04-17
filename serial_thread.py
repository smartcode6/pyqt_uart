# *coding:utf-8 *
from PyQt5.QtCore import QThread,QObject,pyqtSignal
from PyQt5.QtSerialPort import QSerialPort
from time import sleep
import threading
from PyQt5.QtWidgets import QWidget
class MySerial(QObject):
    sig_serial_init=pyqtSignal()
    sig_com_open_close=pyqtSignal(object)
    sig_send_data=pyqtSignal(object)
    sig_recv_data=pyqtSignal(object)
    def __init__(self):
        super(MySerial, self).__init__()
        print('创建了一个串口实例')
    def serial_init(self):
        print("串口线程id:" ,threading.current_thread().ident)
        self.serial=QSerialPort()
        self.serial.readyRead.connect(self.slot_serial_read)
    def slot_serial_com_open_close(self,para):
        print(para)
        if para['flag']==1:
            self.serial.setPortName(para['com'])
            self.serial.setBaudRate(int(para['baud']))
            self.serial.setDataBits(int(para['data']))
            self.serial.setStopBits(int(para['stop']))
            parit=0
            if para['parity']=='None':
                parit=0
            elif para['parity']=='Odd':
                parit=3
            else:
                parit=2
            print(parit)
            self.serial.setParity(parit)
            # 以读写的方式打开
            if self.serial.open(QSerialPort.ReadWrite)==True:
                print('串口打开成功')
            else:
                print('串口打开失败')
        else:
            pass
    def slot_serial_write(self,data):
        print('串口线程待发送的数据' ,data,threading.current_thread().ident)
        send_buff=data['data']
        print(type(send_buff))
        byte_data=str.encode(send_buff)
        print(type(byte_data))
        self.serial.write(byte_data)
        pass
    def slot_serial_read(self):
        print('串口接收到了数据',threading.current_thread().ident)
        recv=self.serial.readAll()
        self.sig_recv_data.emit(recv)
        pass
