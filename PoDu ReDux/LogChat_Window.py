# -*- coding: utf-8 -*-

# Chat implementation generated from reading ui file 'LogChat_Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Chat(object):
    def setupUi(self, Chat):
        Chat.setObjectName("Chat")
        Chat.resize(640, 480)
        self.tabWidget = QtWidgets.QTabWidget(Chat)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.ChatTab = QtWidgets.QWidget()
        self.ChatTab.setObjectName("ChatTab")
        self.ChatWindow = QtWidgets.QTextEdit(self.ChatTab)
        self.ChatWindow.setGeometry(QtCore.QRect(0, 0, 631, 401))
        self.ChatWindow.setStyleSheet("")
        self.ChatWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        self.ChatWindow.setUndoRedoEnabled(False)
        self.ChatWindow.setReadOnly(True)
        self.ChatWindow.setOverwriteMode(True)
        self.ChatWindow.setObjectName("ChatWindow")
        self.ChatEntry = QtWidgets.QLineEdit(self.ChatTab)
        self.ChatEntry.setGeometry(QtCore.QRect(10, 420, 511, 20))
        self.ChatEntry.setStyleSheet("")
        self.ChatEntry.setInputMask("")
        self.ChatEntry.setReadOnly(False)
        self.ChatEntry.setClearButtonEnabled(True)
        self.ChatEntry.setObjectName("ChatEntry")
        self.ChatSend = QtWidgets.QPushButton(self.ChatTab)
        self.ChatSend.setGeometry(QtCore.QRect(530, 420, 101, 21))
        self.ChatSend.setObjectName("ChatSend")
        self.tabWidget.addTab(self.ChatTab, "")
        self.GameLogTab = QtWidgets.QWidget()
        self.GameLogTab.setObjectName("GameLogTab")
        self.GameLog = QtWidgets.QTextEdit(self.GameLogTab)
        self.GameLog.setGeometry(QtCore.QRect(0, 0, 631, 451))
        self.GameLog.setStyleSheet("")
        self.GameLog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.GameLog.setUndoRedoEnabled(False)
        self.GameLog.setReadOnly(True)
        self.GameLog.setOverwriteMode(True)
        self.GameLog.setObjectName("GameLog")
        self.tabWidget.addTab(self.GameLogTab, "")

        self.retranslateUi(Chat)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Chat)

    def retranslateUi(self, Chat):
        _translate = QtCore.QCoreApplication.translate
        Chat.setWindowTitle(_translate("Chat", "Chat"))
        self.ChatWindow.setHtml(_translate("Chat", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.ChatSend.setText(_translate("Chat", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ChatTab), _translate("Chat", "Chat"))
        self.GameLog.setHtml(_translate("Chat", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.GameLogTab), _translate("Chat", "Game Log"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Chat = QtWidgets.QWidget()
    ui = Ui_Chat()
    ui.setupUi(Chat)
    Chat.show()
    sys.exit(app.exec_())
