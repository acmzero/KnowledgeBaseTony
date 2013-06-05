# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon May 27 00:15:54 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys, os
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1024, 720)
        Dialog.setMinimumSize(QtCore.QSize(1024, 720))
        Dialog.setStyleSheet(_fromUtf8("background: white;"))
        Dialog.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setAutoFillBackground(False)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://127.0.0.1:8000/kb")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(Dialog, QtCore.SIGNAL(_fromUtf8("accepted()")), self.webView.reload)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Base de Conocimiento", None))

from PyQt4 import QtWebKit
class ventana(QtGui.QDialog,Ui_Dialog):
  def __init__(self):
    QtGui.QDialog.__init__(self)
    self.setupUi(self)
    
app= QtGui.QApplication(sys.argv)
os.system("echo 'iniciando server' && python2 manage.py runserver 0.0.0.0:8000")
form= ventana()	
form.show()
app.exec_()