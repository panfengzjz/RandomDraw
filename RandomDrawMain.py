# coding: utf-8

import random
import time
import threading
from PyQt5 import QtCore, QtWidgets

import RandomDrawUi

class RandDraw_UI(RandomDrawUi.Ui_Form, QtCore.QObject):
    _time_signal = QtCore.pyqtSignal()
    def signal(self, Form):
        self.start_button.clicked.connect(self.startRandomDraw)
        self.stop_button.clicked.connect(self.stopRandomDraw)
        self._time_signal.connect(self.showNameAndOrder)
    
    def initialize(self):
        self.name_list = []
        self.initNameList()
        self.start_clicked = False;
        self.count_list = [i for i in range(len(self.name_list))]
        self.name_result = [None for _ in range(len(self.name_list))]
        self.init_thread()

    def initNameList(self):
        file_name = "名单.txt"
        f = open(file_name, 'r')
        flines = f.readlines()
        f.close()
        for i in flines:
            if (i.strip() != ""):
                self.name_list.append(i.strip())
        self.name_list = list(set(self.name_list))
        print(self.name_list)
    
    def startRandomDraw(self):
        self.start_clicked = True
        if (len(self.name_list) == 0):
            self.showMessage()
            return
        elif (len(self.name_list) == 1):
            self.pause()
            self.stop_button.click()
            return
        self._time_signal.emit()
        self.resume()
    
    def stopRandomDraw(self):
        if (self.start_clicked == False):
            # ignore the stop clicked signal
            return
        if (len(self.name_list) == 0):
            self.showMessage()
            return
        self.pause()
        item = self.name_list.pop(0)
        order = self.count_list.pop(0)
        self.name_edit.setText(item)
        self.order_edit.setText(str(order+1))
        self.name_result[order] = item

    def showNameAndOrder(self):
        random.shuffle(self.name_list)
        random.shuffle(self.count_list)
        self.name_edit.setText(self.name_list[0])
        self.order_edit.setText(str(self.count_list[0]+1))

    def showNameAndOrderSingal(self):
        while self.__running.isSet():
            self.__flag.wait()        
            while (True):
                self.__flag.wait()
                self._time_signal.emit()
                time.sleep(0.1)
        

    def showMessage(self):
        res = ""
        for i in range(len(self.name_result)):
            res += "{}\t{}\n".format((i+1), self.name_result[i])
       
        QtWidgets.QMessageBox.information(QtWidgets.QWidget(), "抽签结果", res,
                                          QtWidgets.QMessageBox.Ok)
        app = QtWidgets.QApplication.instance()
        app.quit()

    def init_thread(self):
        self.t = threading.Thread(target=self.showNameAndOrderSingal)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.t.setDaemon(True)
        self.t.start()
        self.pause()

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False

if __name__ == "__main__":    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = RandDraw_UI()
    ui.setupUi(Form)
    ui.initialize()
    ui.signal(Form)
    Form.show()
    sys.exit(app.exec_())