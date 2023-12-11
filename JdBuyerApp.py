# -*- coding:utf-8 -*-
import sys
import os
import time
import json
import requests
import traceback

from datetime import datetime

from PySide6.QtCore import Qt, QThread, Signal, QDateTime
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QLineEdit,
    QSlider,
    QPushButton,
    QGridLayout,
    QDateTimeEdit
)

from timer import Timer
from JdSession import Session

NUM_LABEL_FORMAT = '商品购买数量[{0}]个'
STOCK_LABEL_FORMAT = '库存查询间隔[{0}]分'
DATA_FORMAT = '%H:%M:%S'

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

BASE_CITIES = {
    "天津": "3_51035_55897_0",
    "沈阳": "8_560_50821_63242",
    "上海": "2_2813_61125_0",
    "长沙": "18_1482_3606_59998",
    "重庆": "4_48205_71418_0",
    "深圳": "19_1607_3639_59643"
}


def load_area_ids():
    if not os.path.exists('./area_id.json'):
        return
    _cities = {}
    try:
        with open('./area_id.json', 'r', encoding='utf-8') as f:
            for k, v in json.loads(f.read()).items():
                _cities[k] = v
    except Exception as e:
        print(traceback.format_exc())
    return _cities


class JdBuyerUI(QWidget):
    base_cities = BASE_CITIES.copy()

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.ticketThread = TicketThread(self.session)
        self.ticketThread.ticketSignal.connect(self.ticketSignal)
        self.initUI()
        self.loadData()

        for k, v in load_area_ids().items():
            self.base_cities[k] = v

    def loadData(self):
        with open(os.path.join(absPath, 'config.json'), "rb") as f:
            self.config = json.load(f)
        self.skuEdit.setText(self.config.get('skuId'))
        self.areaEdit.setText(self.config.get('areaId'))
        self.stockLabel.setText(STOCK_LABEL_FORMAT.format(self.config.get('freq')))
        self.stockSlider.setValue(self.config.get('freq'))

        self.tokenEdit.setText(self.config.get('pushToken'))

    def saveData(self):
        with open(os.path.join(absPath, 'config.json'), 'w', encoding='utf-8') as f:
            # json.dump(my_list,f)
            # 直接显示中文,不以ASCII的方式显示
            # json.dump(my_list,f,ensure_ascii=False)
            # 显示缩进
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        # 商品SKU
        skuLabel = QLabel('商品SKU(多个请用,号隔开)')
        self.skuEdit = QLineEdit()
        self.skuEdit.setFixedWidth(400)
        grid.addWidget(skuLabel, 1, 0)
        grid.addWidget(self.skuEdit, 1, 1)

        # 区域ID
        areaLabel = QLabel('地区(多个请用,号隔开)')
        self.areaEdit = QLineEdit()
        self.areaEdit.setFixedWidth(400)
        grid.addWidget(areaLabel, 2, 0)
        grid.addWidget(self.areaEdit, 2, 1)

        # 商品查询间隔
        self.stockLabel = QLabel(STOCK_LABEL_FORMAT.format(10))
        self.stockSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.stockSlider.setTickPosition(QSlider.TicksBelow)
        self.stockSlider.setMinimum(10)
        self.stockSlider.setMaximum(60)
        self.stockSlider.valueChanged.connect(self.stockValuechange)
        grid.addWidget(self.stockLabel, 3, 0)
        grid.addWidget(self.stockSlider, 3, 1)

        # pushPlus 的ID
        tokenLabel = QLabel('PushPlus Token')
        self.tokenEdit = QLineEdit()
        self.tokenEdit.setFixedWidth(400)
        grid.addWidget(tokenLabel, 4, 0)
        grid.addWidget(self.tokenEdit, 4, 1)

        # 二维码
        self.qrLabel = QLabel()
        grid.addWidget(self.qrLabel, 5, 0, 1, 2)
        self.qrLabel.hide()

        # 控制按钮
        self.endButton = QPushButton("结束")
        self.endButton.clicked[bool].connect(self.onClick)
        self.startButton = QPushButton("开始")
        self.startButton.clicked[bool].connect(self.onClick)
        grid.addWidget(self.endButton, 6, 0, 1, 2)
        grid.addWidget(self.startButton, 6, 3, 1, 2)

        self.endButton.setDisabled(True)

        # 信息展示
        self.infoLabel = QLabel()
        self.infoLabel.setText("当前登录状态是: {0}".format(
            '已登录' if self.session.isLogin else '未登录'))
        grid.addWidget(self.infoLabel, 7, 0, 2, 4)

        self.setLayout(grid)

        self.setWindowTitle('京东助手')
        self.show()

    # 开启下单任务
    def startTask(self):
        if not self.session.isLogin:
            self.qrLogin()
            self.infoLabel.setText('请使用京东扫码登录')
            return
        sku_id = self.skuEdit.text()
        area_id = self.areaEdit.text()
        push_token = self.tokenEdit.text()
        freq = self.stockSlider.value()

        if not sku_id or not area_id or not push_token or not freq:
            self.infoLabel.setText('填写不完整，不能启动！！！')
            return
        print('area_id:', area_id)
        _area_id = area_id.replace('，', ',')
        _area_id = _area_id.split(',')
        for _a in _area_id:
            if not self.base_cities.get(_a):
                self.infoLabel.setText(f'不支持地区：{_a}')
                return

        self.config['skuId'] = sku_id
        self.config['areaId'] = area_id
        self.config['pushToken'] = push_token
        self.config['freq'] = freq

        self.saveData()
        self.buyerThread = BuyerThread(self.session, self.config)
        self.buyerThread.infoSignal.connect(self.infoSignal)
        self.buyerThread.start()

    # 扫码登录
    def qrLogin(self):
        res = self.session.getQRcode()
        img = QImage.fromData(res)
        self.qrLabel.setPixmap(QPixmap.fromImage(img))
        self.qrLabel.show()
        self.ticketThread.start()

    # 异步线程信号
    def ticketSignal(self, sec):
        self.qrLabel.hide()
        if sec == '成功':
            self.startTask()
        else:
            # 失败
            self.infoLabel.setText(sec)
            self.resumeSatrtBtn()

    def infoSignal(self, sec):
        self.qrLabel.hide()
        self.infoLabel.setText(sec)

    # 按钮监听
    def onClick(self, pressed):
        source = self.sender()
        if source.text() == '开始':

            if not self.skuEdit.text():
                self.infoLabel.setText('请输入需要监控的SKUID')
                return

            self.startTask()
            self.disableStartBtn()
        if source.text() == '结束':
            self.handleStopBrn()

    def handleStopBrn(self):
        if self.session.isLogin:
            self.buyerThread.pause()
        else:
            self.ticketThread.pause()
        self.resumeSatrtBtn()

    def disableStartBtn(self):
        self.endButton.setDisabled(False)
        self.startButton.setDisabled(True)

    def resumeSatrtBtn(self):
        self.endButton.setDisabled(True)
        self.startButton.setDisabled(False)

    def stockValuechange(self):
        stock = self.stockSlider.value()
        self.config['freq'] = stock
        self.stockLabel.setText(STOCK_LABEL_FORMAT.format(stock))


# 登录监控线程


class TicketThread(QThread):
    """ check ticket
    """
    ticketSignal = Signal(str)

    def __init__(self, session):
        super().__init__()
        self.session = session
        self._isPause = False

    def pause(self):
        self._isPause = True

    def run(self):
        self._isPause = False
        ticket = None
        retry_times = 85
        for i in range(retry_times):
            if self._isPause:
                self.ticketSignal.emit('已取消登录')
                return
            ticket = self.session.getQRcodeTicket()
            if ticket:
                break
            time.sleep(2)
        else:
            self.ticketSignal.emit('二维码过期，请重新获取扫描')
            return

        # validate QR code ticket
        if not self.session.validateQRcodeTicket(ticket):
            self.ticketSignal.emit('二维码信息校验失败')
            return

        self.ticketSignal.emit('成功')
        self.session.isLogin = True
        self.session.saveCookies()


# 商品监控线程


class BuyerThread(QThread):
    infoSignal = Signal(str)

    base_cities = BASE_CITIES.copy()

    def __init__(self, session, taskParam):
        super().__init__()
        self.session = session
        self.taskParam = taskParam
        self._isPause = False
        for k, v in load_area_ids().items():
            self.base_cities[k] = v

    def pause(self):
        self._isPause = True

    def run(self):
        sku_ids = self.taskParam.get('skuId')
        sku_ids = sku_ids.replace('，', ',')
        sku_ids = sku_ids.split(',')
        area_id = self.taskParam.get('areaId')
        area_id = area_id.replace('，', ',')
        area_id = area_id.split(',')
        freq = self.taskParam.get('freq')

        self.infoSignal.emit(f'监控中，监控间隔：{freq}分钟')

        while True:
            results = []
            for sku in sku_ids:
                for area in area_id:
                    origin_area = area
                    area = self.base_cities[area]
                    stock = self.session.getItemStock(sku, 1, area)
                    _msg = f'商品ID：{sku}, 地区ID： {area}, 是否有货：{stock}，链接：https://item.jd.com/{sku}.html'
                    print(_msg)
                    results.append({
                        'sku': sku,
                        'area': origin_area,
                        'stock': stock,
                        'link': f'https://item.jd.com/{sku}.html'
                    })
            self.push_message(results)
            print(f'休眠 {freq} 分钟')
            time.sleep(int(freq) * 60)

    def push_message(self, messages: list):
        token = self.taskParam.get('pushToken')  # 在pushpush网站中可以找到
        title = '监控结果'  # 改成你要的标题内容
        content = ''  # 改成你要的正文内容
        for row in messages:
            content += f'#### 商品ID：{row["sku"]} \n' \
                       f'> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' \
                       f'- 地区：{row["area"]} \n' \
                       f'- 是否有货：{row["stock"]} \n' \
                       f'- 链接：{row["link"]} \n' \
                       f'--- \n'

        url = 'http://www.pushplus.plus/send'
        data = {
            "token": token,
            "title": title,
            "content": content,
            'template': 'markdown'
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, data=body, headers=headers)
        print('推送结果：', resp.text)


def main():
    app = QApplication(sys.argv)
    ui = JdBuyerUI()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
