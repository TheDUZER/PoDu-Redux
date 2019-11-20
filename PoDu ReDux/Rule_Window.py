# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Rule_Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Rule(object):
    def setupUi(self, Rule):
        Rule.setObjectName("Rule")
        Rule.resize(240, 320)
        self.buttonBox = QtWidgets.QDialogButtonBox(Rule)
        self.buttonBox.setGeometry(QtCore.QRect(10, 270, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QCheckBox(Rule)
        self.checkBox.setGeometry(QtCore.QRect(30, 50, 81, 20))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Rule)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 100, 81, 20))
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(Rule)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 150, 81, 20))
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(Rule)
        self.checkBox_4.setGeometry(QtCore.QRect(140, 50, 81, 20))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(Rule)
        self.checkBox_5.setGeometry(QtCore.QRect(140, 100, 91, 20))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(Rule)
        self.checkBox_6.setGeometry(QtCore.QRect(140, 150, 91, 20))
        self.checkBox_6.setObjectName("checkBox_6")
        self.label = QtWidgets.QLabel(Rule)
        self.label.setGeometry(QtCore.QRect(80, 10, 81, 16))
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Rule)
        self.radioButton.setGeometry(QtCore.QRect(140, 200, 61, 20))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Rule)
        self.radioButton_2.setGeometry(QtCore.QRect(140, 230, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(Rule)
        self.label_2.setGeometry(QtCore.QRect(20, 200, 101, 51))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Rule)
        self.buttonBox.accepted.connect(Rule.accept)
        self.buttonBox.rejected.connect(Rule.reject)
        QtCore.QMetaObject.connectSlotsByName(Rule)

    def retranslateUi(self, Rule):
        _translate = QtCore.QCoreApplication.translate
        Rule.setWindowTitle(_translate("Rule", "Rule"))
        self.checkBox.setText(_translate("Rule", "Original"))
        self.checkBox_2.setText(_translate("Rule", "New"))
        self.checkBox_3.setText(_translate("Rule", "Custom"))
        self.checkBox_4.setText(_translate("Rule", "Basic Only"))
        self.checkBox_5.setText(_translate("Rule", "No Megas"))
        self.checkBox_6.setText(_translate("Rule", "No Z-Moves"))
        self.label.setText(_translate("Rule", "Rule Settings"))
        self.radioButton.setText(_translate("Rule", "Yes"))
        self.radioButton_2.setText(_translate("Rule", "No"))
        self.label_2.setText(_translate("Rule", "Use updated stats for Original Pokemon?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Rule = QtWidgets.QDialog()
    ui = Ui_Rule()
    ui.setupUi(Rule)
    Rule.show()
    sys.exit(app.exec_())
