# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Library_Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from TeamSave_Dialog import Ui_Save
from TeamMetrics_Dialog import Ui_Metrics

class Ui_Figure_Library(object):
    def openMetrics(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Metrics()
        self.ui.setupUi(self.window)
        self.window.show()
    def openSave(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Save()
        self.ui.setupUi(self.window)
        self.window.show()
    def setupUi(self, Figure_Library):
        Figure_Library.setObjectName("Figure_Library")
        Figure_Library.resize(1289, 907)
        self.LibraryTabs = QtWidgets.QTabWidget(Figure_Library)
        self.LibraryTabs.setGeometry(QtCore.QRect(10, 0, 991, 901))
        self.LibraryTabs.setObjectName("LibraryTabs")
        self.PokemonTab = QtWidgets.QWidget()
        self.PokemonTab.setAccessibleName("")
        self.PokemonTab.setObjectName("PokemonTab")
        self.TypeFilters = QtWidgets.QLabel(self.PokemonTab)
        self.TypeFilters.setGeometry(QtCore.QRect(30, 220, 31, 16))
        self.TypeFilters.setObjectName("TypeFilters")
        self.MovementDisplay = QtWidgets.QLabel(self.PokemonTab)
        self.MovementDisplay.setGeometry(QtCore.QRect(510, 190, 271, 21))
        self.MovementDisplay.setAutoFillBackground(True)
        self.MovementDisplay.setObjectName("MovementDisplay")
        self.layoutWidget = QtWidgets.QWidget(self.PokemonTab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 250, 95, 524))
        self.layoutWidget.setObjectName("layoutWidget")
        self.TypeChecksLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.TypeChecksLayout_2.setContentsMargins(0, 0, 0, 0)
        self.TypeChecksLayout_2.setObjectName("TypeChecksLayout_2")
        self.FightingCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.FightingCheck_2.setChecked(True)
        self.FightingCheck_2.setObjectName("FightingCheck_2")
        self.TypeChecksLayout_2.addWidget(self.FightingCheck_2)
        self.RockCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.RockCheck_2.setChecked(True)
        self.RockCheck_2.setObjectName("RockCheck_2")
        self.TypeChecksLayout_2.addWidget(self.RockCheck_2)
        self.DragonCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.DragonCheck_2.setChecked(True)
        self.DragonCheck_2.setObjectName("DragonCheck_2")
        self.TypeChecksLayout_2.addWidget(self.DragonCheck_2)
        self.GroundCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.GroundCheck_2.setChecked(True)
        self.GroundCheck_2.setObjectName("GroundCheck_2")
        self.TypeChecksLayout_2.addWidget(self.GroundCheck_2)
        self.ElectricCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.ElectricCheck_2.setChecked(True)
        self.ElectricCheck_2.setObjectName("ElectricCheck_2")
        self.TypeChecksLayout_2.addWidget(self.ElectricCheck_2)
        self.PoisonCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.PoisonCheck_2.setChecked(True)
        self.PoisonCheck_2.setObjectName("PoisonCheck_2")
        self.TypeChecksLayout_2.addWidget(self.PoisonCheck_2)
        self.IceCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.IceCheck_2.setChecked(True)
        self.IceCheck_2.setObjectName("IceCheck_2")
        self.TypeChecksLayout_2.addWidget(self.IceCheck_2)
        self.SteelCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.SteelCheck_2.setChecked(True)
        self.SteelCheck_2.setObjectName("SteelCheck_2")
        self.TypeChecksLayout_2.addWidget(self.SteelCheck_2)
        self.FairyCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.FairyCheck_2.setChecked(True)
        self.FairyCheck_2.setObjectName("FairyCheck_2")
        self.TypeChecksLayout_2.addWidget(self.FairyCheck_2)
        self.GrassCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.GrassCheck_2.setChecked(True)
        self.GrassCheck_2.setObjectName("GrassCheck_2")
        self.TypeChecksLayout_2.addWidget(self.GrassCheck_2)
        self.GhostCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.GhostCheck_2.setChecked(True)
        self.GhostCheck_2.setObjectName("GhostCheck_2")
        self.TypeChecksLayout_2.addWidget(self.GhostCheck_2)
        self.PsychicCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.PsychicCheck_2.setChecked(True)
        self.PsychicCheck_2.setTristate(False)
        self.PsychicCheck_2.setObjectName("PsychicCheck_2")
        self.TypeChecksLayout_2.addWidget(self.PsychicCheck_2)
        self.WaterCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.WaterCheck_2.setChecked(True)
        self.WaterCheck_2.setObjectName("WaterCheck_2")
        self.TypeChecksLayout_2.addWidget(self.WaterCheck_2)
        self.FlyingCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.FlyingCheck_2.setChecked(True)
        self.FlyingCheck_2.setObjectName("FlyingCheck_2")
        self.TypeChecksLayout_2.addWidget(self.FlyingCheck_2)
        self.FireCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.FireCheck_2.setChecked(True)
        self.FireCheck_2.setObjectName("FireCheck_2")
        self.TypeChecksLayout_2.addWidget(self.FireCheck_2)
        self.NormalCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.NormalCheck_2.setChecked(True)
        self.NormalCheck_2.setObjectName("NormalCheck_2")
        self.TypeChecksLayout_2.addWidget(self.NormalCheck_2)
        self.DarkCheck_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.DarkCheck_2.setChecked(True)
        self.DarkCheck_2.setObjectName("DarkCheck_2")
        self.TypeChecksLayout_2.addWidget(self.DarkCheck_2)
        self.TypeAll_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.TypeAll_2.setObjectName("TypeAll_2")
        self.TypeChecksLayout_2.addWidget(self.TypeAll_2)
        self.TypeClear_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.TypeClear_2.setObjectName("TypeClear_2")
        self.TypeChecksLayout_2.addWidget(self.TypeClear_2)
        self.PowerFilters = QtWidgets.QLabel(self.PokemonTab)
        self.PowerFilters.setGeometry(QtCore.QRect(110, 430, 121, 16))
        self.PowerFilters.setObjectName("PowerFilters")
        self.PokemonListBox = QtWidgets.QListWidget(self.PokemonTab)
        self.PokemonListBox.setGeometry(QtCore.QRect(250, 130, 181, 681))
        self.PokemonListBox.setObjectName("PokemonListBox")
        self.PokemonNameFilter = QtWidgets.QCheckBox(self.PokemonTab)
        self.PokemonNameFilter.setGeometry(QtCore.QRect(0, 40, 121, 20))
        self.PokemonNameFilter.setChecked(True)
        self.PokemonNameFilter.setObjectName("PokemonNameFilter")
        self.layoutWidget_2 = QtWidgets.QWidget(self.PokemonTab)
        self.layoutWidget_2.setGeometry(QtCore.QRect(500, 250, 331, 561))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.SelectedPokemonTextLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.SelectedPokemonTextLayout_2.setContentsMargins(0, 0, 0, 0)
        self.SelectedPokemonTextLayout_2.setObjectName("SelectedPokemonTextLayout_2")
        self.AbilityText_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.AbilityText_2.setAutoFillBackground(True)
        self.AbilityText_2.setObjectName("AbilityText_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.AbilityText_2)
        self.Attack1Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack1Text_2.setAutoFillBackground(True)
        self.Attack1Text_2.setObjectName("Attack1Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack1Text_2)
        self.Attack2Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack2Text_2.setAutoFillBackground(True)
        self.Attack2Text_2.setObjectName("Attack2Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack2Text_2)
        self.Attack3Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack3Text_2.setAutoFillBackground(True)
        self.Attack3Text_2.setObjectName("Attack3Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack3Text_2)
        self.Attack4Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack4Text_2.setAutoFillBackground(True)
        self.Attack4Text_2.setObjectName("Attack4Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack4Text_2)
        self.Attack5Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack5Text_2.setAutoFillBackground(True)
        self.Attack5Text_2.setObjectName("Attack5Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack5Text_2)
        self.Attack6Check_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack6Check_2.setAutoFillBackground(True)
        self.Attack6Check_2.setObjectName("Attack6Check_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack6Check_2)
        self.Attack7Check_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack7Check_2.setAutoFillBackground(True)
        self.Attack7Check_2.setObjectName("Attack7Check_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack7Check_2)
        self.Attack8Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack8Text_2.setAutoFillBackground(True)
        self.Attack8Text_2.setObjectName("Attack8Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack8Text_2)
        self.Attack9Text_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.Attack9Text_2.setAutoFillBackground(True)
        self.Attack9Text_2.setObjectName("Attack9Text_2")
        self.SelectedPokemonTextLayout_2.addWidget(self.Attack9Text_2)
        self.MovementFilters = QtWidgets.QLabel(self.PokemonTab)
        self.MovementFilters.setGeometry(QtCore.QRect(130, 220, 71, 16))
        self.MovementFilters.setObjectName("MovementFilters")
        self.AbilityTextFilter = QtWidgets.QCheckBox(self.PokemonTab)
        self.AbilityTextFilter.setGeometry(QtCore.QRect(130, 40, 111, 20))
        self.AbilityTextFilter.setObjectName("AbilityTextFilter")
        self.PokemonSearchButton = QtWidgets.QPushButton(self.PokemonTab)
        self.PokemonSearchButton.setGeometry(QtCore.QRect(330, 10, 31, 21))
        self.PokemonSearchButton.setObjectName("PokemonSearchButton")
        self.AttackTextFilter = QtWidgets.QCheckBox(self.PokemonTab)
        self.AttackTextFilter.setGeometry(QtCore.QRect(260, 40, 111, 20))
        self.AttackTextFilter.setObjectName("AttackTextFilter")
        self.MiscFilters = QtWidgets.QLabel(self.PokemonTab)
        self.MiscFilters.setGeometry(QtCore.QRect(30, 110, 55, 16))
        self.MiscFilters.setObjectName("MiscFilters")
        self.FormFilter = QtWidgets.QCheckBox(self.PokemonTab)
        self.FormFilter.setGeometry(QtCore.QRect(120, 140, 91, 21))
        self.FormFilter.setObjectName("FormFilter")
        self.EvolveFilter = QtWidgets.QCheckBox(self.PokemonTab)
        self.EvolveFilter.setGeometry(QtCore.QRect(0, 140, 101, 20))
        self.EvolveFilter.setObjectName("EvolveFilter")
        self.Sprite = QtWidgets.QLabel(self.PokemonTab)
        self.Sprite.setGeometry(QtCore.QRect(520, 45, 141, 141))
        self.Sprite.setObjectName("Sprite")
        self.GlobalFilterReset = QtWidgets.QPushButton(self.PokemonTab)
        self.GlobalFilterReset.setGeometry(QtCore.QRect(0, 790, 221, 28))
        self.GlobalFilterReset.setObjectName("GlobalFilterReset")
        self.PokemonSearchBox = QtWidgets.QLineEdit(self.PokemonTab)
        self.PokemonSearchBox.setGeometry(QtCore.QRect(0, 10, 311, 22))
        self.PokemonSearchBox.setClearButtonEnabled(True)
        self.PokemonSearchBox.setObjectName("PokemonSearchBox")
        self.PokemonListLabel = QtWidgets.QLabel(self.PokemonTab)
        self.PokemonListLabel.setGeometry(QtCore.QRect(300, 110, 81, 16))
        self.PokemonListLabel.setObjectName("PokemonListLabel")
        self.layoutWidget_3 = QtWidgets.QWidget(self.PokemonTab)
        self.layoutWidget_3.setGeometry(QtCore.QRect(120, 250, 95, 173))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.MovmentFilterLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.MovmentFilterLayout_2.setContentsMargins(0, 0, 0, 0)
        self.MovmentFilterLayout_2.setObjectName("MovmentFilterLayout_2")
        self.ZeroMoveCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.ZeroMoveCheck_2.setChecked(True)
        self.ZeroMoveCheck_2.setObjectName("ZeroMoveCheck_2")
        self.MovmentFilterLayout_2.addWidget(self.ZeroMoveCheck_2)
        self.TwoMoveCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.TwoMoveCheck_2.setChecked(True)
        self.TwoMoveCheck_2.setTristate(False)
        self.TwoMoveCheck_2.setObjectName("TwoMoveCheck_2")
        self.MovmentFilterLayout_2.addWidget(self.TwoMoveCheck_2)
        self.ThreePlusMoveCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.ThreePlusMoveCheck_2.setChecked(True)
        self.ThreePlusMoveCheck_2.setObjectName("ThreePlusMoveCheck_2")
        self.MovmentFilterLayout_2.addWidget(self.ThreePlusMoveCheck_2)
        self.OneMoveCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.OneMoveCheck_2.setChecked(True)
        self.OneMoveCheck_2.setObjectName("OneMoveCheck_2")
        self.MovmentFilterLayout_2.addWidget(self.OneMoveCheck_2)
        self.MoveAll_2 = QtWidgets.QPushButton(self.layoutWidget_3)
        self.MoveAll_2.setObjectName("MoveAll_2")
        self.MovmentFilterLayout_2.addWidget(self.MoveAll_2)
        self.MoveClear_2 = QtWidgets.QPushButton(self.layoutWidget_3)
        self.MoveClear_2.setObjectName("MoveClear_2")
        self.MovmentFilterLayout_2.addWidget(self.MoveClear_2)
        self.layoutWidget_4 = QtWidgets.QWidget(self.PokemonTab)
        self.layoutWidget_4.setGeometry(QtCore.QRect(120, 450, 95, 321))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.AttackFilterLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.AttackFilterLayout_2.setContentsMargins(0, 0, 0, 0)
        self.AttackFilterLayout_2.setObjectName("AttackFilterLayout_2")
        self.WCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_4)
        self.WCheck_2.setChecked(True)
        self.WCheck_2.setObjectName("WCheck_2")
        self.AttackFilterLayout_2.addWidget(self.WCheck_2)
        self.GCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_4)
        self.GCheck_2.setChecked(True)
        self.GCheck_2.setObjectName("GCheck_2")
        self.AttackFilterLayout_2.addWidget(self.GCheck_2)
        self.WGMinSpin_2 = QtWidgets.QSpinBox(self.layoutWidget_4)
        self.WGMinSpin_2.setFrame(True)
        self.WGMinSpin_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.WGMinSpin_2.setMaximum(300)
        self.WGMinSpin_2.setObjectName("WGMinSpin_2")
        self.AttackFilterLayout_2.addWidget(self.WGMinSpin_2)
        self.WGMaxSpin_2 = QtWidgets.QSpinBox(self.layoutWidget_4)
        self.WGMaxSpin_2.setFrame(True)
        self.WGMaxSpin_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.WGMaxSpin_2.setMaximum(300)
        self.WGMaxSpin_2.setProperty("value", 300)
        self.WGMaxSpin_2.setObjectName("WGMaxSpin_2")
        self.AttackFilterLayout_2.addWidget(self.WGMaxSpin_2)
        self.WGAttackClear_2 = QtWidgets.QPushButton(self.layoutWidget_4)
        self.WGAttackClear_2.setObjectName("WGAttackClear_2")
        self.AttackFilterLayout_2.addWidget(self.WGAttackClear_2)
        self.PCheck_2 = QtWidgets.QCheckBox(self.layoutWidget_4)
        self.PCheck_2.setChecked(True)
        self.PCheck_2.setObjectName("PCheck_2")
        self.AttackFilterLayout_2.addWidget(self.PCheck_2)
        self.PMinSpin_2 = QtWidgets.QSpinBox(self.layoutWidget_4)
        self.PMinSpin_2.setMinimum(0)
        self.PMinSpin_2.setMaximum(4)
        self.PMinSpin_2.setProperty("value", 0)
        self.PMinSpin_2.setObjectName("PMinSpin_2")
        self.AttackFilterLayout_2.addWidget(self.PMinSpin_2)
        self.PMaxSpin_2 = QtWidgets.QSpinBox(self.layoutWidget_4)
        self.PMaxSpin_2.setMinimum(0)
        self.PMaxSpin_2.setMaximum(4)
        self.PMaxSpin_2.setProperty("value", 4)
        self.PMaxSpin_2.setObjectName("PMaxSpin_2")
        self.AttackFilterLayout_2.addWidget(self.PMaxSpin_2)
        self.PAttackClear_2 = QtWidgets.QPushButton(self.layoutWidget_4)
        self.PAttackClear_2.setObjectName("PAttackClear_2")
        self.AttackFilterLayout_2.addWidget(self.PAttackClear_2)
        self.WheelImage = QtWidgets.QLabel(self.PokemonTab)
        self.WheelImage.setGeometry(QtCore.QRect(720, 50, 171, 141))
        self.WheelImage.setObjectName("WheelImage")
        self.pushButton = QtWidgets.QPushButton(self.PokemonTab)
        self.pushButton.setGeometry(QtCore.QRect(490, 10, 141, 28))
        self.pushButton.setObjectName("pushButton")
        self.LibraryTabs.addTab(self.PokemonTab, "")
        self.PlatesTab = QtWidgets.QWidget()
        self.PlatesTab.setObjectName("PlatesTab")
        self.PlateSearchButton = QtWidgets.QPushButton(self.PlatesTab)
        self.PlateSearchButton.setGeometry(QtCore.QRect(340, 10, 31, 21))
        self.PlateSearchButton.setObjectName("PlateSearchButton")
        self.PlateSearchBox = QtWidgets.QLineEdit(self.PlatesTab)
        self.PlateSearchBox.setGeometry(QtCore.QRect(10, 10, 311, 22))
        self.PlateSearchBox.setClearButtonEnabled(True)
        self.PlateSearchBox.setObjectName("PlateSearchBox")
        self.PlateList = QtWidgets.QListWidget(self.PlatesTab)
        self.PlateList.setGeometry(QtCore.QRect(160, 140, 181, 681))
        self.PlateList.setObjectName("PlateList")
        self.PlateListLabel = QtWidgets.QLabel(self.PlatesTab)
        self.PlateListLabel.setGeometry(QtCore.QRect(210, 110, 81, 16))
        self.PlateListLabel.setObjectName("PlateListLabel")
        self.PlateCostLabel = QtWidgets.QLabel(self.PlatesTab)
        self.PlateCostLabel.setGeometry(QtCore.QRect(20, 110, 61, 16))
        self.PlateCostLabel.setObjectName("PlateCostLabel")
        self.PlateName = QtWidgets.QLabel(self.PlatesTab)
        self.PlateName.setGeometry(QtCore.QRect(440, 110, 91, 16))
        self.PlateName.setObjectName("PlateName")
        self.PlateCost = QtWidgets.QLabel(self.PlatesTab)
        self.PlateCost.setGeometry(QtCore.QRect(440, 150, 55, 16))
        self.PlateCost.setObjectName("PlateCost")
        self.PlateText = QtWidgets.QLabel(self.PlatesTab)
        self.PlateText.setGeometry(QtCore.QRect(440, 210, 251, 111))
        self.PlateText.setObjectName("PlateText")
        self.PlateNameCheck = QtWidgets.QCheckBox(self.PlatesTab)
        self.PlateNameCheck.setGeometry(QtCore.QRect(10, 40, 121, 20))
        self.PlateNameCheck.setChecked(True)
        self.PlateNameCheck.setObjectName("PlateNameCheck")
        self.PlateTextCheck = QtWidgets.QCheckBox(self.PlatesTab)
        self.PlateTextCheck.setGeometry(QtCore.QRect(140, 40, 121, 21))
        self.PlateTextCheck.setChecked(True)
        self.PlateTextCheck.setObjectName("PlateTextCheck")
        self.layoutWidget1 = QtWidgets.QWidget(self.PlatesTab)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 140, 95, 146))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.PlatesCostLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.PlatesCostLayout.setContentsMargins(0, 0, 0, 0)
        self.PlatesCostLayout.setObjectName("PlatesCostLayout")
        self.Plate1CostCheck = QtWidgets.QCheckBox(self.layoutWidget1)
        self.Plate1CostCheck.setChecked(True)
        self.Plate1CostCheck.setObjectName("Plate1CostCheck")
        self.PlatesCostLayout.addWidget(self.Plate1CostCheck)
        self.Plate2CostCheck = QtWidgets.QCheckBox(self.layoutWidget1)
        self.Plate2CostCheck.setChecked(True)
        self.Plate2CostCheck.setObjectName("Plate2CostCheck")
        self.PlatesCostLayout.addWidget(self.Plate2CostCheck)
        self.Plate3CostCheck = QtWidgets.QCheckBox(self.layoutWidget1)
        self.Plate3CostCheck.setChecked(True)
        self.Plate3CostCheck.setObjectName("Plate3CostCheck")
        self.PlatesCostLayout.addWidget(self.Plate3CostCheck)
        self.PlateCostAll = QtWidgets.QPushButton(self.layoutWidget1)
        self.PlateCostAll.setObjectName("PlateCostAll")
        self.PlatesCostLayout.addWidget(self.PlateCostAll)
        self.PlateCostClear = QtWidgets.QPushButton(self.layoutWidget1)
        self.PlateCostClear.setObjectName("PlateCostClear")
        self.PlatesCostLayout.addWidget(self.PlateCostClear)
        self.pushButton_4 = QtWidgets.QPushButton(self.PlatesTab)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 10, 141, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.LibraryTabs.addTab(self.PlatesTab, "")
        self.ZMovesTab = QtWidgets.QWidget()
        self.ZMovesTab.setObjectName("ZMovesTab")
        self.ZmovesLabel = QtWidgets.QLabel(self.ZMovesTab)
        self.ZmovesLabel.setGeometry(QtCore.QRect(100, 60, 81, 16))
        self.ZmovesLabel.setObjectName("ZmovesLabel")
        self.ZmovesList = QtWidgets.QListWidget(self.ZMovesTab)
        self.ZmovesList.setGeometry(QtCore.QRect(50, 90, 181, 681))
        self.ZmovesList.setObjectName("ZmovesList")
        self.ZmoveName = QtWidgets.QLabel(self.ZMovesTab)
        self.ZmoveName.setGeometry(QtCore.QRect(290, 70, 91, 16))
        self.ZmoveName.setObjectName("ZmoveName")
        self.ZmoveText = QtWidgets.QLabel(self.ZMovesTab)
        self.ZmoveText.setGeometry(QtCore.QRect(290, 120, 251, 111))
        self.ZmoveText.setObjectName("ZmoveText")
        self.LibraryTabs.addTab(self.ZMovesTab, "")
        self.listWidget = QtWidgets.QListWidget(Figure_Library)
        self.listWidget.setGeometry(QtCore.QRect(1020, 40, 256, 251))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(Figure_Library)
        self.label.setGeometry(QtCore.QRect(1110, 20, 71, 16))
        self.label.setObjectName("label")
        self.listWidget_2 = QtWidgets.QListWidget(Figure_Library)
        self.listWidget_2.setGeometry(QtCore.QRect(1010, 510, 131, 251))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_2 = QtWidgets.QLabel(Figure_Library)
        self.label_2.setGeometry(QtCore.QRect(1040, 410, 91, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(Figure_Library)
        self.pushButton_2.setGeometry(QtCore.QRect(1017, 300, 130, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Figure_Library)
        self.pushButton_3.setGeometry(QtCore.QRect(1017, 340, 130, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QLineEdit(Figure_Library)
        self.lineEdit.setGeometry(QtCore.QRect(1150, 410, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Figure_Library)
        self.label_3.setGeometry(QtCore.QRect(1040, 450, 55, 16))
        self.label_3.setObjectName("label_3")
        self.listWidget_3 = QtWidgets.QListWidget(Figure_Library)
        self.listWidget_3.setGeometry(QtCore.QRect(1150, 510, 131, 251))
        self.listWidget_3.setObjectName("listWidget_3")
        self.label_4 = QtWidgets.QLabel(Figure_Library)
        self.label_4.setGeometry(QtCore.QRect(1180, 450, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Figure_Library)
        self.label_5.setGeometry(QtCore.QRect(1034, 480, 61, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Figure_Library)
        self.label_6.setGeometry(QtCore.QRect(1180, 480, 55, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_5 = QtWidgets.QPushButton(Figure_Library)
        self.pushButton_5.setGeometry(QtCore.QRect(1167, 300, 110, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Figure_Library)
        self.pushButton_6.setGeometry(QtCore.QRect(1167, 340, 110, 30))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Figure_Library)
        self.pushButton_7.setGeometry(QtCore.QRect(1020, 820, 261, 28))
        self.pushButton_7.setObjectName("pushButton_7")

        self.retranslateUi(Figure_Library)
        self.pushButton_6.clicked.connect(self.openSave)
        self.pushButton_7.clicked.connect(self.openMetrics)
        self.LibraryTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Figure_Library)

    def retranslateUi(self, Figure_Library):
        _translate = QtCore.QCoreApplication.translate
        Figure_Library.setWindowTitle(_translate("Figure_Library", "Libraries"))
        self.TypeFilters.setText(_translate("Figure_Library", "Type"))
        self.MovementDisplay.setText(_translate("Figure_Library", "Movement"))
        self.FightingCheck_2.setText(_translate("Figure_Library", "Fighting"))
        self.RockCheck_2.setText(_translate("Figure_Library", "Rock"))
        self.DragonCheck_2.setText(_translate("Figure_Library", "Dragon"))
        self.GroundCheck_2.setText(_translate("Figure_Library", "Ground"))
        self.ElectricCheck_2.setText(_translate("Figure_Library", "Electric"))
        self.PoisonCheck_2.setText(_translate("Figure_Library", "Poison"))
        self.IceCheck_2.setText(_translate("Figure_Library", "Ice"))
        self.SteelCheck_2.setText(_translate("Figure_Library", "Steel"))
        self.FairyCheck_2.setText(_translate("Figure_Library", "Fairy"))
        self.GrassCheck_2.setText(_translate("Figure_Library", "Grass"))
        self.GhostCheck_2.setText(_translate("Figure_Library", "Ghost"))
        self.PsychicCheck_2.setText(_translate("Figure_Library", "Psychic"))
        self.WaterCheck_2.setText(_translate("Figure_Library", "Water"))
        self.FlyingCheck_2.setText(_translate("Figure_Library", "Flying"))
        self.FireCheck_2.setText(_translate("Figure_Library", "Fire"))
        self.NormalCheck_2.setText(_translate("Figure_Library", "Normal"))
        self.DarkCheck_2.setText(_translate("Figure_Library", "Dark"))
        self.TypeAll_2.setText(_translate("Figure_Library", "Select All"))
        self.TypeClear_2.setText(_translate("Figure_Library", "Clear"))
        self.PowerFilters.setText(_translate("Figure_Library", "Attacks and Ranges"))
        self.PokemonNameFilter.setText(_translate("Figure_Library", "Search Pokemon"))
        self.AbilityText_2.setText(_translate("Figure_Library", "Ability Text"))
        self.Attack1Text_2.setText(_translate("Figure_Library", "Attack1"))
        self.Attack2Text_2.setText(_translate("Figure_Library", "Attack2"))
        self.Attack3Text_2.setText(_translate("Figure_Library", "Attack3"))
        self.Attack4Text_2.setText(_translate("Figure_Library", "Attack4"))
        self.Attack5Text_2.setText(_translate("Figure_Library", "Attack5"))
        self.Attack6Check_2.setText(_translate("Figure_Library", "Attack6"))
        self.Attack7Check_2.setText(_translate("Figure_Library", "Attack7"))
        self.Attack8Text_2.setText(_translate("Figure_Library", "Attack8"))
        self.Attack9Text_2.setText(_translate("Figure_Library", "Attack9"))
        self.MovementFilters.setText(_translate("Figure_Library", "Movement"))
        self.AbilityTextFilter.setText(_translate("Figure_Library", "Search Abilities"))
        self.PokemonSearchButton.setText(_translate("Figure_Library", "Go"))
        self.AttackTextFilter.setText(_translate("Figure_Library", "Search Attacks"))
        self.MiscFilters.setText(_translate("Figure_Library", "Misc."))
        self.FormFilter.setText(_translate("Figure_Library", "Form Only"))
        self.EvolveFilter.setText(_translate("Figure_Library", "Evolve Only"))
        self.Sprite.setText(_translate("Figure_Library", "Sprite"))
        self.GlobalFilterReset.setText(_translate("Figure_Library", "Reset All Filters"))
        self.PokemonSearchBox.setText(_translate("Figure_Library", "Search..."))
        self.PokemonListLabel.setText(_translate("Figure_Library", "Pokemon List"))
        self.ZeroMoveCheck_2.setText(_translate("Figure_Library", "0"))
        self.TwoMoveCheck_2.setText(_translate("Figure_Library", "2"))
        self.ThreePlusMoveCheck_2.setText(_translate("Figure_Library", "3+"))
        self.OneMoveCheck_2.setText(_translate("Figure_Library", "1"))
        self.MoveAll_2.setText(_translate("Figure_Library", "Select All"))
        self.MoveClear_2.setText(_translate("Figure_Library", "Clear"))
        self.WCheck_2.setText(_translate("Figure_Library", "White"))
        self.GCheck_2.setText(_translate("Figure_Library", "Gold"))
        self.WGAttackClear_2.setText(_translate("Figure_Library", "Clear"))
        self.PCheck_2.setText(_translate("Figure_Library", "Purple"))
        self.PAttackClear_2.setText(_translate("Figure_Library", "Clear"))
        self.WheelImage.setText(_translate("Figure_Library", "Wheel"))
        self.pushButton.setText(_translate("Figure_Library", "Add to Team >>>"))
        self.LibraryTabs.setTabText(self.LibraryTabs.indexOf(self.PokemonTab), _translate("Figure_Library", "Pokemon"))
        self.PlateSearchButton.setText(_translate("Figure_Library", "Go"))
        self.PlateSearchBox.setText(_translate("Figure_Library", "Search..."))
        self.PlateListLabel.setText(_translate("Figure_Library", "Plate List"))
        self.PlateCostLabel.setText(_translate("Figure_Library", "Cost"))
        self.PlateName.setText(_translate("Figure_Library", "Plate Name"))
        self.PlateCost.setText(_translate("Figure_Library", "Plate Cost"))
        self.PlateText.setText(_translate("Figure_Library", "Plate Text"))
        self.PlateNameCheck.setText(_translate("Figure_Library", "Search Name"))
        self.PlateTextCheck.setText(_translate("Figure_Library", "Search Text"))
        self.Plate1CostCheck.setText(_translate("Figure_Library", "1"))
        self.Plate2CostCheck.setText(_translate("Figure_Library", "2"))
        self.Plate3CostCheck.setText(_translate("Figure_Library", "3"))
        self.PlateCostAll.setText(_translate("Figure_Library", "Select All"))
        self.PlateCostClear.setText(_translate("Figure_Library", "Clear"))
        self.pushButton_4.setText(_translate("Figure_Library", "Add to Plates >>>"))
        self.LibraryTabs.setTabText(self.LibraryTabs.indexOf(self.PlatesTab), _translate("Figure_Library", "Plates"))
        self.ZmovesLabel.setText(_translate("Figure_Library", "Z-Moves"))
        self.ZmoveName.setText(_translate("Figure_Library", "Z-Move Name"))
        self.ZmoveText.setText(_translate("Figure_Library", "Plate Text"))
        self.LibraryTabs.setTabText(self.LibraryTabs.indexOf(self.ZMovesTab), _translate("Figure_Library", "Z-Moves"))
        self.label.setText(_translate("Figure_Library", "Team List"))
        self.label_2.setText(_translate("Figure_Library", "Selected Team:"))
        self.pushButton_2.setText(_translate("Figure_Library", "Select Team"))
        self.pushButton_3.setText(_translate("Figure_Library", "Save Team"))
        self.label_3.setText(_translate("Figure_Library", "Pokemon"))
        self.label_4.setText(_translate("Figure_Library", "Plates"))
        self.label_5.setText(_translate("Figure_Library", "Slots: x/6"))
        self.label_6.setText(_translate("Figure_Library", "Cost: x/8"))
        self.pushButton_5.setText(_translate("Figure_Library", "New Team..."))
        self.pushButton_6.setText(_translate("Figure_Library", "Save Team As..."))
        self.pushButton_7.setText(_translate("Figure_Library", "Team Metrics"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Figure_Library = QtWidgets.QWidget()
    ui = Ui_Figure_Library()
    ui.setupUi(Figure_Library)
    Figure_Library.show()
    sys.exit(app.exec_())