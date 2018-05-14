from toolsmac import Ui_MainWindow

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QDesktopWidget, QTableWidgetItem, QHeaderView)
import requests
from sshtunnel import SSHTunnelForwarder
import pymysql

login_cell="8613472876201" #登录账号手机号
login_token="123456"   #登录验证码
channel="IOS"     #登录消息报头传递channel字段 "ANDROID" "IOS"
platform="WEB"    #登录消息报头传递platorm字段 "KINGKONG" "WEB"
#file = 'C:/Users/langlive15/Desktop/qa_rsa/qa_rsa'
file='qss/qa_rsa'#rsa文件地址
address = "test-be-mysql.cw3afzr4cznt.ap-northeast-1.rds.amazonaws.com"    #服务器地址
userid='user_app'      #mysql 登录名
password='51e4dbe0_bccd426b!98c6.8817ccc0f981'    #mysql 密码


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.lg)
        self.pushButton.clicked.connect(self.copytext)
        self.pushButton_3.clicked.connect(self.plus)
        self.pushButton_4.clicked.connect(self.plusitem)
        self.pushButton_5.clicked.connect(self.newwindow)
        self.pushButton_6.clicked.connect(self.liveid)
        self.pushButton_7.clicked.connect(self.copytext1)
        self.pushButton_8.clicked.connect(self.info)
        self.setWindowIcon(QtGui.QIcon('img/123.png'))



    def lg(self):
            self.tw = 'TW +886'
            self.cn = 'CN +86'
            self.hk = 'HK +852'
            self.mc = 'MC +853'
            self.sg = 'SG +65'
            self.my = 'MY +60'

            lcid = self.lineEdit.text()  # 获取文本框内容
            if lcid == '':
                #pass
                QtWidgets.QMessageBox.information(self, "Tips", "账号不能为空")
            elif str(lcid).isdigit() == False:
                QtWidgets.QMessageBox.information(self, "Tips", "账号只能为数字，请重新输入数字")

                self.lineEdit.clear()
            else:
                comboid = self.comboBox.currentText()
                if comboid == self.tw:
                    comboid = int(886)
                if comboid == self.cn:
                    comboid = int(86)
                if comboid == self.hk:
                    comboid = int(852)
                if comboid == self.mc:
                    comboid = int(853)
                if comboid == self.sg:
                    comboid = int(65)
                if comboid == self.my:
                    comboid = int(60)

                url = "https://api.s.lang.live/v2/passport/mobile"
                data = {
                    "cell": int(str(comboid) + lcid),
                    "token": login_token
                }
                print(data)
                headers = {'CHANNEL': channel,
                           'PLATFORM': platform,
                           'Content-Type': 'application/x-www-form-urlencoded'}
                r = requests.post(url=url, data=data, headers=headers)
                print(type(r.json()))
                QtWidgets.QMessageBox.information(self, "Tips", "登录成功！")

                self.lineEdit_2.setText(str(r.json()['data']['pfid']))
                self.lineEdit_3.setText(str(r.json()['data']['access_token']))

    def copytext(self):

        clipboard = QtWidgets.QApplication.clipboard()  # 调用剪贴板
        clipboard.setText(self.lineEdit_3.text())
        if self.lineEdit_3.text() != '':
            QtWidgets.QMessageBox.information(self, "Tips", "复制成功！")

    def plus(self):
        pfid = self.lineEdit_4.text()
        monkey = self.lineEdit_5.text()

        if pfid == '' :
            QtWidgets.QMessageBox.information(self, "Tips", "账号不能为空")
        elif str(pfid).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", "账号只能为数字，请重新输入数字")
            self.lineEdit_4.clear()
        if monkey == '':
            QtWidgets.QMessageBox.information(self, "Tips", "浪花不能为空")
        elif str(monkey).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", "浪花只能为数字，请重新输入数字")
            self.lineEdit_5.clear()
        else:
             with SSHTunnelForwarder(
                    ('13.112.45.12', 22),  # B机器的配置
                    ssh_pkey=file,
                    # ssh_password=flie,
                    ssh_username="cainiaodj",
                    remote_bind_address=(address, 3306)) as server:  # A机器的配置

                conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                       port=server.local_bind_port,
                                       user=userid,
                                       passwd=password,
                                       # db='db_admin',
                                       charset='utf8')

                cursor = conn.cursor()
                sql = "select db_member_01.tb_user.pfid  from db_member_01.tb_user  where db_member_01.tb_user.pfid=" + self.lineEdit_4.text()

                print (sql)
                cursor.execute(sql)
                result6 = cursor.fetchall()
                print (result6)
                conn.close()
                li = []
                list1 = list(result6)
                li.append(list1)
                li2 = str(li).replace("[", "").replace("]", "")
                print (li2)
                if li2 == '':
                    QtWidgets.QMessageBox.information(self, "Tips", "账号不存在，请先注册")
                    self.lineEdit_4.clear()
                else:
                    url1 = "https://api.s.lang.live/dd/balance/add"
                    data1 = {
                        "pfid": int(str(pfid)),
                        "key": "flzx3qc",
                        "gold": int(str(monkey))
                    }
                    print (data1)
                    headers1 = {'Content-Type': 'application/x-www-form-urlencoded'}
                    r1 = requests.post(url=url1, data=data1, headers=headers1)
                    print (r1.json())
                    print (r1.json()['balance'])
                    QtWidgets.QMessageBox.information(self, "Tips", self.tr('当前账号：  ' + pfid + "  \n增加的浪花为  " + monkey + " \n现有的浪花为  " + r1.json()['balance']))

    def plusitem(self):
        pfid1 = self.lineEdit_6.text()
        itemid = self.lineEdit_7.text()
        numid = self.lineEdit_8.text()

        if pfid1 == '':
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("账号不能为空"))
        elif str(pfid1).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("账号只能为数字，请重新输入数字"))
            self.lineEdit_6.clear()
        if itemid == '':
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("背包道具编号不能为空"))
        elif str(itemid).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("背包道具编号只能为数字，请重新输入数字"))
            self.lineEdit_7.clear()
        if numid == '':
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("背包道具数量不能为空"))
        elif str(numid).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("背包道具数量只能为数字，请重新输入数字"))
            self.lineEdit_8.clear()


        else:

            with SSHTunnelForwarder(
                    ('13.112.45.12', 22),  # B机器的配置
                    ssh_pkey=file,
                    # ssh_password=flie,
                    ssh_username="cainiaodj",
                    remote_bind_address=(address, 3306)) as server:  # A机器的配置

                conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                       port=server.local_bind_port,
                                       user=userid,
                                       passwd=password,
                                       # db='db_admin',
                                       charset='utf8')

                cursor = conn.cursor()
                sql = "select db_member_01.tb_user.pfid  from db_member_01.tb_user  where db_member_01.tb_user.pfid=" + pfid1
                print(sql)
                cursor.execute(sql)
                result7 = cursor.fetchall()
                print(result7)
                conn.close()
                li = []
                list3 = list(result7)
                li.append(list3)
                # print "+++++",type(li)
                li2 = str(li).replace("[", "").replace("]", "")
                print(li2)
                if li2 == '':
                    QtWidgets.QMessageBox.information(self, "Tips", self.tr("账号不存在，请先注册"))
                    self.lineEdit_6.clear()
                else:
                    url2 = "https://api.s.lang.live/v2/bag/debug_add"
                    data2 = {
                        "pfid": int(str(pfid1)),
                        "item_id": int(str(itemid)),
                        "item_num": int(str(numid))
                    }
                    print(data2)
                    headers2 = {'Content-Type': 'application/x-www-form-urlencoded'}
                    r2 = requests.post(url=url2, data=data2, headers=headers2)
                    print(r2.json())

                    with SSHTunnelForwarder(
                            ('13.112.45.12', 22),  # B机器的配置
                            ssh_pkey=file,
                            # ssh_password=flie,
                            ssh_username="cainiaodj",
                            remote_bind_address=(address, 3306)) as server:  # A机器的配置

                        conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                               port=server.local_bind_port,
                                               user=userid,
                                               passwd=password,
                                               # db='db_admin',
                                               charset='utf8')

                        cursor = conn.cursor()

                        # print type(li)

                        print(itemid)
                        sql = "select db_billing.tb_bag_item.item_type  from db_billing.tb_bag_item where db_billing.tb_bag_item.id=" + itemid
                        sql1 = "select db_billing.tb_bag_item.alert_desc from db_billing.tb_bag_item where db_billing.tb_bag_item.id=" + itemid
                        print(sql)
                        cursor.execute(sql)
                        print("+++",sql)
                        result0 = cursor.fetchall()
                        print(result0)
                        print(result0[0])
                        cursor.execute(sql1)
                        result1 = cursor.fetchall()
                        # conn.close()
                        li = []
                        list1 = list(result0[0])
                        li.append(list1)
                        # print "+++++",type(li)
                        li2 = str(li)
                        li3 = li2.replace("[", "").replace("]", "")
                        if li3 == '3':
                            li3 = '称号道具'
                        if li3 == '2':
                            li3 = '人气道具'
                        if li3 == '1':
                            li3 = '普通道具'
                        print(li3)
                        li1 = []
                        list2 = list(result1[0])
                        li1.append(list2)
                        # print "+++++", type(li1)
                        li4 = li1
                        print(li4)
                        li5 = str(li4).replace("u", "").replace("\'", "").replace(u"使用", "").replace(u"是否", "").replace("[", "").replace("]","").replace("?", "")
                        print(li5)
                        li6 = li5
                        conn.close()
                        # conn.close()
                        # print sql
                        QtWidgets.QMessageBox.information(self, "Tips", self.tr('当前账号：  ' + pfid1 + "   \n道具名称为    " + li6 + "  \n道具类型为 " + li3 + "\n增加数量为  " + numid + "  个"))

    def liveid(self):
        pfid2 = self.lineEdit_9.text()

        if pfid2 == '':
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("账号不能为空"))
        elif str(pfid2).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("账号只能为数字，请重新输入数字"))
            self.lineEdit_9.clear()

        else:

            with SSHTunnelForwarder(
                    ('13.112.45.12', 22),  # B机器的配置
                    ssh_pkey=file,
                    # ssh_password=flie,
                    ssh_username="cainiaodj",
                    remote_bind_address=(address, 3306)) as server:  # A机器的配置

                conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                       port=server.local_bind_port,
                                       user=userid,
                                       passwd=password,
                                       # db='db_admin',
                                       charset='utf8')

                cursor = conn.cursor()
                print(pfid2)
                sql = "select db_global.tb_live_log.pfid from db_global.tb_live_log where db_global.tb_live_log.pfid=" + pfid2 + ' ORDER BY auto_id desc limit 1'
                sql1 = "select db_global.tb_live_log.live_id from db_global.tb_live_log where db_global.tb_live_log.pfid=" + pfid2 + ' ORDER BY auto_id desc limit 1'
                sql2 = "select db_global.tb_live_log.play_id from db_global.tb_live_log where db_global.tb_live_log.pfid=" + pfid2 + ' ORDER BY auto_id desc limit 1'
                print(sql)
                print(sql1)
                print(sql2)
                cursor.execute(sql)
                result0 = cursor.fetchall()
                cursor.execute(sql1)
                result1 = cursor.fetchall()
                cursor.execute(sql2)
                result2 = cursor.fetchall()
                print(result0)
                print(result1)
                print(result2)
                li = []
                list1 = list(result0)
                li.append(list1)
                # print "+++++",type(li)
                li2 = str(li)
                li3 = li2.replace("[", "").replace("]", "")
                print('+++',li3)
                if li3=='':
                    QtWidgets.QMessageBox.information(self, "Tips", self.tr("账号不存在，请先注册"))
                    self.lineEdit_9.clear()

                else:

                    lii = []
                    list2 = list(result1[0])
                    lii.append(list2)
                     # print "+++++",type(li)
                    li4 = str(lii)
                    li5 = li4.replace("[", "").replace("]", "").replace("\'", "")
                    print(li5)
                    liii = []
                    list3 = list(result2[0])
                    liii.append(list3)
                    # print "+++++",type(li)
                    li6 = str(liii)
                    li7 = li6.replace("[", "").replace("]", "").replace("\'", "")
                    print(li7)

                    if li3=='None':
                        self.lineEdit_10.setText(str(li7))


                    else:
                        QtWidgets.QMessageBox.information(self, "Tips", self.tr("当前账号未在开播，请先开播\n上一次开播的live_id为"+ li5))
                        self.lineEdit_10.clear()

    def copytext1(self):

        clipboard = QtWidgets.QApplication.clipboard()  # 调用剪贴板
        clipboard.setText(self.lineEdit_10.text())
        if self.lineEdit_10.text() != '':
            QtWidgets.QMessageBox.information(self, "Tips", "复制成功！")

    def info(self):
        pfid3= self.lineEdit_11.text()


        if self.lineEdit_11.text() == '':
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("pfid不能为空"))
        elif str(self.lineEdit_11.text()).isdigit() == False:
            QtWidgets.QMessageBox.information(self, "Tips", self.tr("pfid只能为数字，请重新输入数字"))
            self.lineEdit_11.clear()
        else:

            with SSHTunnelForwarder(
                    ('13.112.45.12', 22),  # B机器的配置
                    ssh_pkey=file,
                    # ssh_password=flie,
                    ssh_username="cainiaodj",
                    remote_bind_address=(address, 3306)) as server:  # A机器的配置

                conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                       port=server.local_bind_port,
                                       user=userid,
                                       passwd=password,
                                       # db='db_admin',
                                       charset='utf8')

                cursor = conn.cursor()
                print(pfid3)
                sql = "select db_member_01.tb_user.uid from db_member_01.tb_user  where db_member_01.tb_user.pfid=" + pfid3
                sql1 = "select db_member_01.tb_user.nickname from db_member_01.tb_user where db_member_01.tb_user.pfid=" + pfid3
                sql2 = "select db_member_01.tb_user.sex from db_member_01.tb_user where db_member_01.tb_user.pfid=" + pfid3
                sql3 = "select db_member_01.tb_user.sex from db_member_01.tb_user where db_member_01.tb_user.pfid=" + pfid3
                print(sql)
                print(sql1)
                print(sql2)
                cursor.execute(sql)
                result0 = cursor.fetchall()
                cursor.execute(sql1)
                result1 = cursor.fetchall()
                cursor.execute(sql2)
                result2 = cursor.fetchall()
                print(result0)
                print(result1)
                print(result2)
                li = []
                list1 = list(result0)
                li.append(list1)
                # print "+++++",type(li)
                li2 = str(li)
                li3 = li2.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").replace("'", "")
                print('+++', li3)
                self.lineEdit_12.setText(str(li3))
                if li3 == '':
                    QtWidgets.QMessageBox.information(self, "Tips", self.tr("pfid不存在，请先注册"))
                    self.lineEdit_11.clear()

                else:
                    lii = []
                    list2 = list(result1[0])
                    lii.append(list2)
                    # print "+++++",type(li)
                    li4 = str(lii)
                    li5 = li4.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").replace("'", "")
                    print(li5)
                    liii = []
                    list3 = list(result2[0])
                    liii.append(list3)
                    # print "+++++",type(li)
                    li6 = str(liii)
                    li7 = li6.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "")
                    print(li7)
                    if li7 == '1':
                       li7 = '男'
                    if li7 == '2':
                       li7 = '女'
                    if li7 == '0':
                       li7 = '秘密'
                    self.lineEdit_13.setText(str(li5))
                    self.lineEdit_14.setText(str(li7))


    def newwindow(self):
        self.new = self.table()
        self.new.show()


    class table(QtWidgets.QMainWindow, Ui_MainWindow):
       def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle(u'背包道具列表')
            self.setWindowIcon(QtGui.QIcon(':/img/123.png'))
            self.table = QTableWidget(500, 9)
            self.resize(919, 799)
            self.setCentralWidget(self.table)

            with SSHTunnelForwarder(
                    ('13.112.45.12', 22),  # B机器的配置
                    ssh_pkey=file,
                    # ssh_password=flie,
                    ssh_username="cainiaodj",
                    remote_bind_address=(address, 3306)) as server:  # A机器的配置

                conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                       port=server.local_bind_port,
                                       user=userid,
                                       passwd=password,
                                       # db='db_admin',
                                       charset='utf8')

                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                data = cursor.fetchone()
                # print "Database version : %s " % data
                sql = "select  db_billing.tb_bag_item.id from db_billing.tb_bag_item GROUP BY db_billing.tb_bag_item.id Asc"
                sql1 = "select  db_billing.tb_bag_item.item_type from db_billing.tb_bag_item GROUP BY db_billing.tb_bag_item.id Asc"
                sql2 = "select  db_billing.tb_bag_item.alert_desc from db_billing.tb_bag_item GROUP BY db_billing.tb_bag_item.id Asc"

                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.execute(sql1)
                result1 = cursor.fetchall()
                cursor.execute(sql2)
                result2 = cursor.fetchall()
                conn.close()
            a = self.class_li(result)
            b = self.class_lii(result1)
            c = self.class_lii(result2)
            self.table.verticalHeader().setVisible(False)
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)

            self.table.setColumnWidth(0, 45)
            self.table.setColumnWidth(3, 45)
            self.table.setColumnWidth(6, 45)
            self.table.setColumnWidth(1, 80)
            self.table.setColumnWidth(4, 80)
            self.table.setColumnWidth(7, 80)
            self.table.setColumnWidth(2, 190)
            self.table.setColumnWidth(5, 190)
            self.table.setColumnWidth(8, 190)

            self.table.setAlternatingRowColors(True)
            self.table.setHorizontalHeaderLabels([u'编号', u'类型', u'道具名', u'编号', u'类型', u'道具名', u'编号', u'类型', u'道具名'])
            # self.table.horizontalHeader().setStretchLastSection(True)

            x = 0
            y = 0
            for i in a:
                newItem = QTableWidgetItem(i)
                self.table.setItem(x, y, newItem)
                y = y + 3
                if y >= 9:
                    y = 0
                    x = x + 1
            x = 0
            z = 1
            for i in b:
                if i == '3':
                    i = u'称号道具'
                if i == '2':
                    i = u'人气道具'
                if i == '1':
                    i = u'普通道具'
                newItem1 = QTableWidgetItem(i)
                self.table.setItem(x, z, newItem1)
                z = z + 3
                if z >= 9:
                    z = 1
                    x = x + 1
            x = 0
            v = 2
            for i in c:

                newItem1 = QTableWidgetItem(i)

                self.table.setItem(x, v, newItem1)

                v = v + 3
                if v >= 9:
                    v = 2
                    x = x + 1

       def class_li(self, results):
           arr = []
           for x in range(len(results)):
               li = []
               list1 = list(results[x])
               li.append(list1)
               li2 = str(li)
               li3 = li2.replace("[", "").replace("]", "").replace("?", "").replace("L", "")
               li4 = (li3).replace("u", "").replace("\'", "").replace(u"使用", "").replace(u"是否", "")
               data = (li4)
               arr.append(data)
           return arr

       def class_lii(self, results):
           arr = []
           for x in range(len(results)):
               li = []
               # print type(li)
               list1 = list(results[x])
               li.append(list1)
               # print "+++++",type(li)
               li2 = str(li)
               # print "+++++",(li2)
               li3 = li2.replace("[", "").replace("]", "").replace("?", "").replace("？", "")
               li4 = li3.replace("u", "").replace("\'", "").replace(u"使用","").replace(u"是否","")
               # print unicode(li3,'utf8').decode('utf8')
               # unicode(self.Edit5.text()).encode('utf-8')
               # print li4

               data = (li4)
               arr.append(data)
         # print type(arr)
           return arr

