# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TeamSave_Save.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName("Save")
        Save.resize(240, 148)
        self.buttonBox = QtWidgets.QDialogButtonBox(Save)
        self.buttonBox.setGeometry(QtCore.QRect(0, 90, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(Save)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 201, 22))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Save)
        self.buttonBox.accepted.connect(Save.accept)
        self.buttonBox.rejected.connect(Save.reject)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        _translate = QtCore.QCoreApplication.translate
        Save.setWindowTitle(_translate("Save", "Save"))
        self.lineEdit.setText(_translate("Save", "Team Name..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Save = QtWidgets.QDialog()
    ui = Ui_Save()
    ui.setupUi(Save)
    Save.show()
    sys.exit(app.exec_())
