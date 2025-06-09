# -*-coding:utf-8-*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QLabel, QComboBox, \
    QTextBrowser, QDesktopWidget, QVBoxLayout, QWidget, QTabWidget, QCheckBox, QProgressBar, QHBoxLayout, QLineEdit

from PyQt5 import QtCore
import api
import PyQt5.QtGui as ag
from PyQt5.QtCore import QThread, pyqtSignal
from Qss import SharedStyle


class LoadingThread(QThread):
    loading_finished = pyqtSignal()

    def run(self):
        # 模拟加载过程，这里可以替换为实际的加载操作
        import time
        time.sleep(2)

        # 发送加载完成信号
        self.loading_finished.emit()


class tool:

    def __init__(self):

        self.accessToken = None  # 初始化全局变量
        self.jobUuid = None
        self.appliction_list = None
        self.taskId = None
        self.applictionAllData = None
        self.applicationName = None
        self.robotUuid = None
        self.canshu = None
        self.accountName = None
        self.line_edits = []
        self.param = None

        self.window = QMainWindow()  # 主窗口
        self.window.resize(500, 600)
        self.window.setWindowTitle('影刀可视化调度神器')
        self.window.setWindowIcon(ag.QIcon('robot.ico'))
        screen = QDesktopWidget().screenGeometry()  # 获取屏幕大小
        x = int((screen.width() - self.window.width()) / 2)  # 计算窗口居中时的左上角坐标
        y = int((screen.height() - self.window.height()) / 2)
        self.window.move(x, y)  # 将窗口移动到屏幕中央

        tab_widget = QTabWidget()  # 选项卡
        self.window.setCentralWidget(tab_widget)
        SharedStyle.menuBar(tab_widget)
        tab1 = QWidget()  # 创建选项卡页1
        tab_widget.addTab(tab1, "应用调度")
        tab2 = QWidget()  # 创建选项卡页2
        tab_widget.addTab(tab2, "任务调度")

        # 在选项卡页1中添加控件
        self.account = QLabel()  # 文字：影刀账号
        self.account.setGeometry(QtCore.QRect(40, 40, 100, 41))
        self.account.setText('机器人账号:')
        self.textEdit = QPlainTextEdit()
        self.textEdit.setPlaceholderText("例如xxx@xxx")
        self.textEdit.setGeometry(QtCore.QRect(180, 50, 260, 35))
        self.id = QLabel()  # id
        self.id.setGeometry(QtCore.QRect(40, 100, 100, 41))
        self.id.setText('accessId:')
        self.textEdit2 = QPlainTextEdit()
        self.textEdit2.setPlaceholderText("在控制台获取")
        self.textEdit2.setGeometry(QtCore.QRect(180, 100, 260, 35))
        self.access_secret = QLabel()  # secret
        self.access_secret.setGeometry(QtCore.QRect(40, 150, 130, 41))
        self.access_secret.setText('accessSecret:')
        self.textEdit3 = QPlainTextEdit()
        self.textEdit3.setPlaceholderText("在控制台获取")
        self.textEdit3.setGeometry(QtCore.QRect(180, 150, 260, 35))
        self.select = QLabel()  # 选择应用
        self.select.setGeometry(QtCore.QRect(40, 200, 100, 41))
        self.select.setText('选择应用:')
        self.textEdit4 = QComboBox()
        self.textEdit4.setGeometry(QtCore.QRect(180, 200, 260, 35))
        self.button_stop = QPushButton('停止应用')  # 停止应用、启动应用、重试应用
        self.button_stop.move(40, 260)
        self.button_stop.clicked.connect(self.stop)
        self.button_start = QPushButton('启动应用')
        self.button_start.move(150, 260)
        self.button_flesh = QPushButton('刷新应用')
        self.button_flesh.move(260, 260)
        self.button_flesh.clicked.connect(self.flesh)
        self.selectCanshu = QCheckBox('流程参数')
        self.selectCanshu.setChecked(False)
        self.selectCanshu.move(370, 260)
        self.selectCanshu.stateChanged.connect(self.checkbox_state_changed)
        self.state = QLabel()  # 运行状态
        self.state.setGeometry(QtCore.QRect(40, 320, 100, 41))
        self.state.setText('运行状态:')
        self.textEdit5 = QTextBrowser()
        self.textEdit5.setPlaceholderText("接口返回数据")
        self.textEdit5.setGeometry(QtCore.QRect(40, 370, 400, 200))

        SharedStyle.applyStyle(self.button_stop)  # 应用样式
        SharedStyle.applyStyle(self.button_start)
        SharedStyle.applyStyle(self.button_flesh)
        SharedStyle.textStyle(self.textEdit)
        SharedStyle.textStyle(self.textEdit2)
        SharedStyle.textStyle(self.textEdit3)
        self.timer = QtCore.QTimer()  # 创建定时器对象
        self.timer.timeout.connect(self.button_start_handler)  # 将定时器的timeout信号连接到self.button_start方法
        self.button_start.clicked.connect(self.start)  # 将按钮的clicked信号连接到self.start方法
        self.account.setParent(tab1)  # 控件绑定到tab页
        self.id.setParent(tab1)
        self.textEdit2.setParent(tab1)
        self.textEdit3.setParent(tab1)
        self.access_secret.setParent(tab1)
        self.select.setParent(tab1)
        self.textEdit.setParent(tab1)
        self.textEdit4.setParent(tab1)
        self.button_stop.setParent(tab1)
        self.button_start.setParent(tab1)
        self.button_flesh.setParent(tab1)
        self.state.setParent(tab1)
        self.textEdit5.setParent(tab1)
        self.selectCanshu.setParent(tab1)

        # 在选项卡页2中添加控件
        # 文字：scheduleUuid
        self.scheduleUuidTab2 = QLabel(self.window)
        self.scheduleUuidTab2.setGeometry(QtCore.QRect(40, 40, 100, 41))
        self.scheduleUuidTab2.setText('任务id:')
        self.textEditTab2 = QPlainTextEdit()
        self.textEditTab2.setPlaceholderText("在控制台获取")
        self.textEditTab2.setGeometry(QtCore.QRect(180, 50, 260, 35))
        # id
        self.idTab2 = QLabel()
        self.idTab2.setGeometry(QtCore.QRect(40, 100, 100, 41))
        self.idTab2.setText('accessId:')
        self.textEdit2Tab2 = QPlainTextEdit()
        self.textEdit2Tab2.setPlaceholderText("在控制台获取")
        self.textEdit2Tab2.setGeometry(QtCore.QRect(180, 100, 260, 35))
        # secret
        self.access_secretTab2 = QLabel()
        self.access_secretTab2.setGeometry(QtCore.QRect(40, 150, 130, 41))
        self.access_secretTab2.setText('accessSecret:')
        self.textEdit3Tab2 = QPlainTextEdit()
        self.textEdit3Tab2.setPlaceholderText("在控制台获取")
        self.textEdit3Tab2.setGeometry(QtCore.QRect(180, 150, 260, 35))
        # 停止应用、启动应用、重试应用
        self.button_stopTab2 = QPushButton('停止任务')
        self.button_stopTab2.move(40, 260)
        self.button_stopTab2.clicked.connect(self.stopTab2)
        self.button_startTab2 = QPushButton('启动任务')
        self.button_startTab2.move(150, 260)

        # 运行状态
        self.stateTab2 = QLabel()
        self.stateTab2.setGeometry(QtCore.QRect(40, 320, 100, 41))
        self.stateTab2.setText('运行状态:')
        self.textEdit5Tab2 = QTextBrowser()
        self.textEdit5Tab2.setPlaceholderText("接口返回数据")
        self.textEdit5Tab2.setGeometry(QtCore.QRect(40, 370, 400, 200))
        # 创建定时器对象
        self.timerTab2 = QtCore.QTimer()
        # 将定时器的timeout信号连接到self.button_start方法
        self.timerTab2.timeout.connect(self.button_start_handlerTab2)
        # 将按钮的clicked信号连接到self.start方法
        self.button_startTab2.clicked.connect(self.startTab2)

        SharedStyle.textStyle(self.textEditTab2)
        SharedStyle.textStyle(self.textEdit2Tab2)
        SharedStyle.textStyle(self.textEdit3Tab2)
        SharedStyle.selectStyle(self.textEdit4)

        self.scheduleUuidTab2.setParent(tab2)
        self.idTab2.setParent(tab2)
        self.textEdit2Tab2.setParent(tab2)
        self.textEdit3Tab2.setParent(tab2)
        self.access_secretTab2.setParent(tab2)
        self.textEditTab2.setParent(tab2)
        self.button_stopTab2.setParent(tab2)
        self.button_startTab2.setParent(tab2)
        self.stateTab2.setParent(tab2)
        self.textEdit5Tab2.setParent(tab2)

    def flesh(self):
        self.accessKeyId = self.textEdit2.toPlainText()
        self.accessKeySecret = self.textEdit3.toPlainText()
        self.accessToken = api.getAccessToken(self.accessKeyId, self.accessKeySecret)
        if type(self.accessToken) != str or self.accessToken == """'data'""":
            self.textEdit5.append('请检查id或secret是否正确！')
            self.textEdit5.ensureCursorVisible()
        else:
            data = api.queryAllApplication(self.accessToken)
            appliction_list = data['应用列表']
            self.applictionAllData = data['完整信息']
            self.textEdit4.addItems(appliction_list)

    def checkbox_state_changed(self):
        if self.selectCanshu.isChecked():

            screen = QDesktopWidget().screenGeometry()
            x = int((screen.width() - self.window.width()) / 2)
            y = int((screen.height() - self.window.height()) / 2)
            self.window2 = QMainWindow()
            self.window2.resize(500, 600)
            self.window2.move(x + 500, y)
            self.window2.setWindowTitle('流程参数配置界面')
            self.window2.setWindowIcon(ag.QIcon('鸡腿.ico'))

            # 创建容器部件和布局
            self.container_widget = QWidget()
            self.layout = QVBoxLayout(self.container_widget)
            # 设置容器部件为中心部件
            self.window2.setCentralWidget(self.container_widget)

            # 创建加载特效部件
            self.loading_widget = QProgressBar()

            self.loading_widget.setRange(0, 0)  # 设置范围为0-0，表示无限循环
            self.loading_widget.setHidden(True)
            self.layout.addWidget(self.loading_widget)

            # 创建刷新按钮
            self.refresh_button = QPushButton("动态刷新流程参数", self.window2)
            self.refresh_button.clicked.connect(self.refresh_button_clicked)
            self.layout.addWidget(self.refresh_button)

            # 创建输入框和标签的容器
            self.input_container = QWidget(self.window2)
            self.input_layout = QVBoxLayout(self.input_container)
            self.layout.addWidget(self.input_container)

            # 创建加载线程
            self.loading_thread = None
            self.window2.show()
        else:
            self.window2.close()

    def refresh_button_clicked(self):
        # # 清空文本框列表
        self.line_edits = []
        # 停止之前的加载线程
        if self.loading_thread and self.loading_thread.isRunning():
            self.loading_thread.quit()
            self.loading_thread.wait()
        self.applicationName = self.textEdit4.currentText()
        try:
            self.robotUuid = [x for x in self.applictionAllData if x['应用名称'] == self.applicationName][0]['robotUuid']
            self.canshu = api.query_RobotParam(self.accessToken, self.robotUuid)[0]
            print(self.canshu)
            self.generate_input_boxes()
        except Exception:
            self.textEdit5.append('请检查所填参数是否正确！')
            self.textEdit5.ensureCursorVisible()

    def generate_input_boxes(self):
        # 清空输入框和标签容器中的内容
        while self.input_layout.count() > 0:
            layout_item = self.input_layout.itemAt(0)
            layout = layout_item.layout()
            while layout.count() > 0:
                item = layout.itemAt(0)
                widget = item.widget()
                layout.removeWidget(widget)
                widget.setParent(None)
                # 释放内存
                widget.deleteLater()
            self.input_layout.removeItem(layout_item)

        # 显示加载特效
        self.loading_widget.setHidden(False)

        # 创建加载线程
        self.loading_thread = LoadingThread()
        self.loading_thread.loading_finished.connect(self.loading_finished)
        self.loading_thread.start()

    def loading_finished(self):
        # 隐藏加载特效
        self.loading_widget.setHidden(True)
        self.line_edits = []  # 清空文本框列表
        if self.canshu == None:
            self.textEdit5.append('该应用没有流程参数！')
            self.textEdit5.ensureCursorVisible()
        else:
            # 根据数据生成输入框和标签
            for item in self.canshu:
                layout = QHBoxLayout()

                text_label = QLabel(f"{item['name']} ({item['type']})")
                layout.addWidget(text_label)

                line_edit = QLineEdit()
                line_edit.setText(item['value'])
                layout.addWidget(line_edit)

                self.input_layout.addLayout(layout)
                # 将文本框添加到列表
                self.line_edits.append([text_label, line_edit])
            self.textEdit5.append('已动态获取应用的流程参数（入参）！')
            self.textEdit5.ensureCursorVisible()

        # 更新窗口布局
        self.layout.addStretch()

    def get_values_button_clicked(self):
        # 获取文本框值
        values = []
        for line_edit in self.line_edits:
            value0 = line_edit[0].text()
            valueName = value0.split(' (')[0]
            valueType = value0.split(' (')[1].split(')')[0]
            value1 = line_edit[1].text()
            values.append([valueName, valueType, value1])

        for i in values:
            if i[1] == 'str':
                continue
            elif i[1] == 'bool':
                values[values.index(i)][2] = bool(values[values.index(i)][2])
            elif i[1] == 'int':
                values[values.index(i)][2] = int(values[values.index(i)][2])
            elif i[1] == 'float':
                values[values.index(i)][2] = float(values[values.index(i)][2])
        self.param = [
            {"name": x[0], "value": x[2], "type": x[1]} for x in values]




    def start(self):
        # 启动定时器
        try:
            self.get_values_button_clicked()
            self.applicationName = self.textEdit4.currentText()
            self.robotUuid = [x for x in self.applictionAllData if x['应用名称'] == self.applicationName][0][
                'robotUuid']
            self.accountName = self.textEdit.toPlainText()
            self.jobUuid = api.startJob(self.accessToken, self.robotUuid, self.accountName,param=self.param)
            self.timer.start(2000)
        except Exception as e:
            print(e)
            print('ywt')
            self.textEdit5.append('请检查所填参数是否正确！')
            self.textEdit5.ensureCursorVisible()

    def button_start_handler(self):
        # 定时器的timeout信号处理函数
        response = api.query(self.accessToken, self.jobUuid)
        print("状态：" + response)
        if response == 'error':
            print('应用运行异常！请检查入参或者指令ya！')
            self.textEdit5.append('应用运行异常！请检查入参或者指令！' + "状态：" + response)
            self.textEdit5.ensureCursorVisible()
        elif response == 'finish':
            print('应用运行完成，调度结束！')
            self.textEdit5.append('应用运行完成，调度结束！' + "状态：" + response)
            self.textEdit5.ensureCursorVisible()
            # 停止定时器
            self.timer.stop()
        else:
            print('应用还在运行中.......')
            self.textEdit5.append('应用还在运行中.......' + "状态：" + response)
            self.textEdit5.ensureCursorVisible()
            scrollbar = self.textEdit5.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def stop(self):
        self.timer.stop()
        data = api.job_stop(self.accessToken, self.jobUuid)['success']
        if data == True:
            self.textEdit5.append('应用已停止运行！')
            self.textEdit5.ensureCursorVisible()
        else:
            self.textEdit5.append('请检查所填参数是否正确！')
            self.textEdit5.ensureCursorVisible()

    def startTab2(self):
        # 启动定时器
        self.taskId = self.textEditTab2.toPlainText()
        self.accessKeyId = self.textEdit2Tab2.toPlainText()
        self.accessKeySecret = self.textEdit3Tab2.toPlainText()
        self.accessToken = api.getAccessToken(self.accessKeyId, self.accessKeySecret)
        self.taskUuid = api.startScheduleUuid(self.accessToken, self.taskId)
        self.timerTab2.start(2000)

    def button_start_handlerTab2(self):
        # 定时器的timeout信号处理函数
        response = api.queryJobStatus(self.accessToken, self.taskUuid)
        print("状态：" + response)
        if response == 'error':
            print('任务运行异常！请检查入参或者指令！')
            self.textEdit5Tab2.append('任务运行异常！请检查入参或者指令！' + "状态：" + response)
            self.textEdit5Tab2.ensureCursorVisible()
        elif response == 'finish':
            print('任务运行完成，调度结束！')
            self.textEdit5Tab2.append('任务运行完成，调度结束！' + "状态：" + response)
            self.textEdit5Tab2.ensureCursorVisible()
            # 停止定时器
            self.timerTab2.stop()
        else:
            print('任务还在运行中.......')
            self.textEdit5Tab2.append('任务还在运行中.......' + "状态：" + response)
            self.textEdit5Tab2.ensureCursorVisible()



    def stopTab2(self):
        self.timerTab2.stop()
        data = api.taskStop(self.accessToken, self.taskUuid)['success']
        print(data, type(str(data)))
        if data == True:
            self.textEdit5Tab2.append('任务已停止运行！')
            self.textEdit5Tab2.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication([])
    file_tidy = tool()
    # apply_stylesheet(app, theme='dark_blue.xml')
    file_tidy.window.show()

    app.exec_()
